from __future__ import annotations

from typing import Callable, Awaitable, Any, Optional, Dict, List, Tuple
from dataclasses import dataclass, field

from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from persistence.persistence_layer import PersistenceLayer
from spark.state import SparkState

# Type aliases for clarity
HandlerFunc = Callable[[SparkState, PersistenceLayer], Awaitable[dict]]
FactoryResult = Tuple[Dict[str, Any], HandlerFunc]
FactoryFunc = Callable[[], FactoryResult]

@dataclass
class PhaseDefinition:
    name: str
    base_aspect_factory: Optional[FactoryFunc] = None
    aspect_factories: List[FactoryFunc] = field(default_factory=list)
    policy_config: Dict[str, Any] = field(default_factory=dict)
    is_meta: bool = False

class SpiralBuilder:
    def __init__(self):
        self._phases: List[PhaseDefinition] = []
        self._current_phase: Optional[PhaseDefinition] = None
    
    def phase(self, name: str) -> SpiralBuilder:
        self._current_phase = PhaseDefinition(name=name)
        self._phases.append(self._current_phase)
        return self

    def meta_phase(self, name: str) -> SpiralBuilder:
        self._current_phase = PhaseDefinition(name=name, is_meta=True)
        self._phases.append(self._current_phase)
        return self

    def base_aspect(self, factory: FactoryFunc) -> SpiralBuilder:
        if self._current_phase:
            self._current_phase.base_aspect_factory = factory
        return self

    def aspects(self, *factories: FactoryFunc) -> SpiralBuilder:
        if self._current_phase:
            self._current_phase.aspect_factories.extend(factories)
        return self

    def policy(self, **kwargs) -> SpiralBuilder:
        if self._current_phase:
            self._current_phase.policy_config.update(kwargs)
        return self

    def build(self, persistence: Optional[PersistenceLayer] = None) -> CompiledStateGraph:
        workflow = StateGraph(SparkState)
        
        # We need a dummy entry point or the first phase is the entry point
        # Assuming the first defined phase is the entry point.
        
        previous_node_name = None
        
        for phase_def in self._phases:
            node_name = phase_def.name
            
            # Construct the handler for this phase node
            # This handler will execute base_aspect and aspects, and process proposals
            phase_handler = self._create_phase_handler(phase_def, persistence)
            
            workflow.add_node(node_name, phase_handler)
            
            if previous_node_name:
                workflow.add_edge(previous_node_name, node_name)
            else:
                workflow.set_entry_point(node_name)
                
            previous_node_name = node_name
            
        if previous_node_name:
            workflow.add_edge(previous_node_name, END)
            
        return workflow.compile()

    def _create_phase_handler(self, phase_def: PhaseDefinition, persistence: Optional[PersistenceLayer]):
        """
        Creates a single node handler that orchestrates the execution of aspects 
        and integration of their results.
        """
        
        # Instantiate handlers
        handlers = []
        phase_metas = {} # Store metadata if needed
        
        if phase_def.base_aspect_factory:
            meta, handler = phase_def.base_aspect_factory()
            handlers.append((meta, handler))
            phase_metas[meta.get("id", "base")] = meta
            
        for factory in phase_def.aspect_factories:
            meta, handler = factory()
            handlers.append((meta, handler))
            phase_metas[meta.get("id", "aspect")] = meta
            
        async def node_entry(state: SparkState) -> dict:
            # Execute all handlers (sequentially or parallel?)
            # Prompt implies we need to integrate results. 
            # Let's run them and collect results.
            
            # Note: The node function in LangGraph usually receives the state.
            # Our handlers expect (DialogState, PersistenceLayer).
            # We need to inject persistence if available.
            
            results = []
            # Using partial functionality since handlers are async
            for meta, handler in handlers:
                # Assuming handler signature is (state, persistence)
                res = await handler(state, persistence) # type: ignore
                results.append((meta, res))
                
            # Process proposals / integrate results
            combined_update = {}
            for meta, res in results:
                processed_res = self._process_proposals(phase_def.name, meta, res, state)
                combined_update.update(processed_res)
                
            return combined_update

        return node_entry

    def _process_proposals(self, phase_name: str, meta: dict, result: dict, state: SparkState) -> dict:
        """
        Process proposals from handlers and integrate into state.
        Mapping logic based on returned keys and meta information.
        """
        updates = {}
        
        # Merge the raw result first (default behavior)
        updates.update(result)
        
        from dialog.models import IntentionDescriptor
        
        # Specific proposal processing logic
        # If result contains keys for IntentionDescriptor, construct it.
        # Check if result has keys 'categories', 'vectors', 'summary', 'reasoning'
        if all(k in result for k in ("categories", "vectors", "summary", "reasoning")):
             # Create IntentionDescriptor
             try:
                 descriptor = IntentionDescriptor(**result)
                 # Determine where to put it. 
                 # If meta id is "meta.learn" or generic, putting in meta_intention_descriptor or intention_descriptor
                 # SparkState has 'meta_intention_descriptor'.
                 # Let's assign it there.
                 updates["meta_intention_descriptor"] = descriptor
                 
                 # Clean up raw keys if we consumed them? 
                 # Usually we might keep them or remove them. LangGraph merges updates.
                 # If we return "categories": ..., it will try to set state.categories.
                 # SparkState DOES NOT have "categories" field. 
                 # So we MUST remove them from the update if SparkState is strict (Pydantic is strict by default on extra fields? No, depends on config, but usually fails or ignores).
                 # Better to remove consumed keys.
                 for k in ("categories", "vectors", "summary", "reasoning"):
                     del updates[k]
                     
             except Exception as e:
                 print(f"Error creating IntentionDescriptor: {e}")
        
        return updates
