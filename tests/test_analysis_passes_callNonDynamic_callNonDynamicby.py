

from unittest.mock import MagicMock, patch
import openunderstand.analysis_passes.callNonDynamic_callNonDynamicby as module_0


def test_case_0():
    
    listener = module_0.CallNonDynamicAndCallNonDynamicBy()
    assert isinstance(listener.implement, list)
    assert len(listener.implement) == 0


class BlockStatement1Context:
    pass

def test_case_1_kill_implement_init_mutant():
    """Kills mutant where self.implement in __init__ is modified or set to None."""
    listener = module_0.CallNonDynamicAndCallNonDynamicBy()

    mock_ctx = MagicMock()
    mock_ctx.EXTENDS.return_value = True

    mock_body = MagicMock()
    mock_member = MagicMock()
    mock_method = MagicMock()
    mock_block = MagicMock()

    mock_body.memberDeclaration.return_value = mock_member
    mock_member.methodDeclaration.return_value = mock_method
    mock_method.methodBody().block.return_value = mock_block
    mock_ctx.classBody().classBodyDeclaration.return_value = [mock_body]

    # Real class instance so type(bStatement).__name__ actually matches "BlockStatement1Context"
    mock_bstatement = BlockStatement1Context()

    mock_statement = MagicMock()
    mock_bstatement.statement = MagicMock(return_value=mock_statement)
    mock_statement.statement = None

    mock_exp = MagicMock()
    mock_exp2 = MagicMock()
    mock_primary = MagicMock()
    mock_super = MagicMock()
    mock_method_call = MagicMock()

    mock_statement.expression.return_value = mock_exp
    mock_exp.expression.return_value = mock_exp2
    mock_exp2.primary.return_value = mock_primary
    mock_primary.SUPER.return_value = mock_super

    mock_exp.methodCall.return_value = mock_method_call
    mock_method_call.IDENTIFIER.return_value = "superMethod"
    mock_method_call.start.line = 10
    mock_method_call.start.column = 4

    mock_block.blockStatement.return_value = [mock_bstatement]

    with patch(
        "openunderstand.analysis_passes.class_properties.ClassPropertiesListener.findParents",
        return_value=["pkg", "MyClass"],
    ), patch(
        "openunderstand.analysis_passes.class_properties.ClassPropertiesListener.findClassOrInterfaceModifiers",
        return_value=["public"],
    ):
        listener.enterClassDeclaration(mock_ctx)

    assert listener.implement is not None
    assert len(listener.implement) == 1
    assert listener.implement[0]["type_ent_longname"] == "superMethod"