from __future__ import annotations
from typing import Callable, Awaitable, Any, Optional, Dict, List
from dataclasses import dataclass, field
import asyncio

from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from dialog.state import DialogState
from persistence.persistence_layer import PersistenceLayer

# Type aliases for clarity
HandlerFunc = Callable[[DialogState, PersistenceLayer], Awaitable[dict]]
FactoryFunc = Callable[[], HandlerFunc]

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
        workflow = StateGraph(DialogState)
        
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
        if phase_def.base_aspect_factory:
            handlers.append(phase_def.base_aspect_factory())
        for factory in phase_def.aspect_factories:
            handlers.append(factory())
            
        async def node_entry(state: DialogState) -> dict:
            # Execute all handlers (sequentially or parallel?)
            # Prompt implies we need to integrate results. 
            # Let's run them and collect results.
            
            # Note: The node function in LangGraph usually receives the state.
            # Our handlers expect (DialogState, PersistenceLayer).
            # We need to inject persistence if available.
            # If persistence is not passed to build(), we might need a workaround or assume it's not used by these specific handlers 
            # (though the signature in dialog/graph.py uses it).
            # For now, I'll pass None if not provided, or better, require it in build() or handle it.
            # But StateGraph nodes only take state (and config).
            # If handlers need persistence, it typically must be passed via some context or closure.
            # Here I am capturing `persistence` from `build` scope.
            
            results = []
            # Using partial functionality since handlers are async
            for handler in handlers:
                # Assuming handler signature is (state, persistence)
                # If persistence is None, we might error if handler expects it.
                # But let's assume valid persistence is passed to build OR handled gracefully.
                res = await handler(state, persistence) # type: ignore
                results.append(res)
                
            # Process proposals / integrate results
            # The prompt says: "results should be integrated back into LangGraph graph state via corresponding ... proposal processor functions"
            # We need to merge the dicts returned by handlers into the state.
            # LangGraph automagically merges dict updates if they match state keys.
            # BUT the prompt mentions "proposal processors". 
            # This implies complex logic: raw result -> processor -> state update.
            
            combined_update = {}
            for res in results:
                # Here we would look up a processor for the keys in 'res'
                # For this implementation, I will assume a default "merge" processor behavior 
                # unless I find specific processor definitions.
                # Since I don't have the processor registry, I will implement a generic integration
                # that updates the state with the keys returned.
                
                # If there are specific keys that need "proposal processing", we'd do it here.
                # I'll add a hook for it.
                processed_res = self._process_proposals(phase_def.name, res, state)
                combined_update.update(processed_res)
                
            return combined_update

        return node_entry

    def _process_proposals(self, phase_name: str, result: dict, state: DialogState) -> dict:
        """
        Mock implementation of proposal processing.
        In a real scenario, this would look up processors based on keys in `result` 
        and the current `phase_name`.
        """
        # For now, just pass through. 
        # The user prompt mentions "functions processors proposals" (plural).
        # We assume direct mapping for now.
        return result
