"""The action definition for the SysML toolbox."""

from typing import Sequence, Tuple

from gaphas.item import SE

import gaphor.UML.diagramitems as diagramitems
from gaphor import UML, diagram
from gaphor.core import gettext
from gaphor.diagram.diagramtoolbox import ToolboxDefinition, ToolDef
from gaphor.diagram.diagramtools import PlacementTool


def namespace_config(new_item):
    subject = new_item.subject
    diagram = new_item.canvas.diagram
    subject.package = diagram.namespace
    subject.name = f"New{type(subject).__name__}"


def initial_pseudostate_config(new_item):
    new_item.subject.kind = "initial"


def history_pseudostate_config(new_item):
    new_item.subject.kind = "shallowHistory"


def metaclass_config(new_item):
    namespace_config(new_item)
    new_item.subject.name = "Class"


# Actions: ((section (name, label, icon_name, shortcut)), ...)
sysml_toolbox_actions: ToolboxDefinition = (
    (
        gettext("General"),
        (
            ToolDef(
                "toolbox-pointer",
                gettext("Pointer"),
                "gaphor-pointer-symbolic",
                "Escape",
                item_factory=None,
            ),
            ToolDef(
                "toolbox-line",
                gettext("Line"),
                "gaphor-line-symbolic",
                "l",
                PlacementTool.new_item_factory(diagram.general.Line),
            ),
            ToolDef(
                "toolbox-box",
                gettext("Box"),
                "gaphor-box-symbolic",
                "b",
                PlacementTool.new_item_factory(diagram.general.Box),
                SE,
            ),
            ToolDef(
                "toolbox-ellipse",
                gettext("Ellipse"),
                "gaphor-ellipse-symbolic",
                "e",
                PlacementTool.new_item_factory(diagram.general.Ellipse),
                SE,
            ),
            ToolDef(
                "toolbox-comment",
                gettext("Comment"),
                "gaphor-comment-symbolic",
                "k",
                PlacementTool.new_item_factory(
                    diagram.general.CommentItem, UML.Comment
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-comment-line",
                gettext("Comment line"),
                "gaphor-comment-line-symbolic",
                "<Shift>K",
                PlacementTool.new_item_factory(diagram.general.CommentLineItem),
            ),
        ),
    ),
    (
        gettext("Blocks"),
        (
            ToolDef(
                "toolbox-class",
                gettext("Class"),
                "gaphor-class-symbolic",
                "c",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.ClassItem, UML.Class, config_func=namespace_config
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-interface",
                gettext("Interface"),
                "gaphor-interface-symbolic",
                "i",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.InterfaceItem,
                    UML.Interface,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-package",
                gettext("Package"),
                "gaphor-package-symbolic",
                "p",
                PlacementTool.new_item_factory(
                    diagramitems.PackageItem, UML.Package, config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-association",
                gettext("Association"),
                "gaphor-association-symbolic",
                "<Shift>A",
                PlacementTool.new_item_factory(diagramitems.AssociationItem),
            ),
            ToolDef(
                "toolbox-dependency",
                gettext("Dependency"),
                "gaphor-dependency-symbolic",
                "<Shift>D",
                PlacementTool.new_item_factory(diagramitems.DependencyItem),
            ),
            ToolDef(
                "toolbox-generalization",
                gettext("Generalization"),
                "gaphor-generalization-symbolic",
                "<Shift>G",
                PlacementTool.new_item_factory(diagramitems.GeneralizationItem),
            ),
            ToolDef(
                "toolbox-implementation",
                gettext("Implementation"),
                "gaphor-implementation-symbolic",
                "<Shift>I",
                PlacementTool.new_item_factory(diagramitems.ImplementationItem),
            ),
        ),
    ),
    (
        gettext("Actions"),
        (
            ToolDef(
                "toolbox-action",
                gettext("Action"),
                "gaphor-action-symbolic",
                "a",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.ActionItem, UML.Action, config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-initial-node",
                gettext("Initial node"),
                "gaphor-initial-node-symbolic",
                "j",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.InitialNodeItem, UML.InitialNode
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-activity-final-node",
                gettext("Activity final node"),
                "gaphor-activity-final-node-symbolic",
                "f",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.ActivityFinalNodeItem, UML.ActivityFinalNode
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-flow-final-node",
                gettext("Flow final node"),
                "gaphor-flow-final-node-symbolic",
                "w",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.FlowFinalNodeItem, UML.FlowFinalNode
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-decision-node",
                gettext("Decision/merge node"),
                "gaphor-decision-node-symbolic",
                "g",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.DecisionNodeItem, UML.DecisionNode
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-fork-node",
                gettext("Fork/join node"),
                "gaphor-fork-node-symbolic",
                "<Shift>R",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.ForkNodeItem, UML.JoinNode
                ),
                handle_index=1,
            ),
            ToolDef(
                "toolbox-object-node",
                gettext("Object node"),
                "gaphor-object-node-symbolic",
                "<Shift>O",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.ObjectNodeItem,
                    UML.ObjectNode,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-partition",
                gettext("Partition"),
                "gaphor-partition-symbolic",
                "<Shift>P",
                item_factory=PlacementTool.new_item_factory(diagramitems.PartitionItem),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-flow",
                gettext("Control/object flow"),
                "gaphor-control-flow-symbolic",
                "<Shift>F",
                item_factory=PlacementTool.new_item_factory(diagramitems.FlowItem),
            ),
            ToolDef(
                "toolbox-send-signal-action",
                gettext("Send signal action"),
                "gaphor-send-signal-action-symbolic",
                None,
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.SendSignalActionItem,
                    UML.SendSignalAction,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-accept-event-action",
                gettext("Accept event action"),
                "gaphor-accept-event-action-symbolic",
                None,
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.AcceptEventActionItem,
                    UML.AcceptEventAction,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
        ),
    ),
    (
        gettext("States"),
        (
            ToolDef(
                "toolbox-state",
                gettext("State"),
                "gaphor-state-symbolic",
                "s",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.StateItem, UML.State, config_func=namespace_config
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-initial-pseudostate",
                gettext("Initial Pseudostate"),
                "gaphor-initial-pseudostate-symbolic",
                "<Shift>S",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.InitialPseudostateItem,
                    UML.Pseudostate,
                    initial_pseudostate_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-final-state",
                gettext("Final State"),
                "gaphor-final-state-symbolic",
                "x",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.FinalStateItem, UML.FinalState
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-history-pseudostate",
                gettext("History Pseudostate"),
                "gaphor-pseudostate-symbolic",
                "q",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.HistoryPseudostateItem,
                    UML.Pseudostate,
                    history_pseudostate_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-transition",
                gettext("Transition"),
                "gaphor-transition-symbolic",
                "<Shift>T",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.TransitionItem
                ),
            ),
        ),
    ),
    (
        gettext("Use Cases"),
        (
            ToolDef(
                "toolbox-use-case",
                gettext("Use case"),
                "gaphor-use-case-symbolic",
                "u",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.UseCaseItem, UML.UseCase, config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-actor",
                gettext("Actor"),
                "gaphor-actor-symbolic",
                "t",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.ActorItem, UML.Actor, config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-use-case-association",
                gettext("Association"),
                "gaphor-association-symbolic",
                "<Shift>B",
                item_factory=PlacementTool.new_item_factory(
                    diagramitems.AssociationItem
                ),
            ),
            ToolDef(
                "toolbox-include",
                gettext("Include"),
                "gaphor-include-symbolic",
                "<Shift>U",
                item_factory=PlacementTool.new_item_factory(diagramitems.IncludeItem),
            ),
            ToolDef(
                "toolbox-extend",
                gettext("Extend"),
                "gaphor-extend-symbolic",
                "<Shift>X",
                item_factory=PlacementTool.new_item_factory(diagramitems.ExtendItem),
            ),
        ),
    ),
)
