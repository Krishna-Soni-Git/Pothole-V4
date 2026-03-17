import libcst as cst

class DictToLiteralTransformer(cst.CSTTransformer):
    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        # Check if this is a dict() call
        if isinstance(updated_node.func, cst.Name) and updated_node.func.value == "dict":
            # Only convert if all arguments are keyword arguments
            if all(isinstance(arg.keyword, cst.Name) for arg in updated_node.args):
                elements = []
                for arg in updated_node.args:
                    key = arg.keyword.value
                    elements.append(cst.DictElement(
                        key=cst.SimpleString(value=f'"{key}"'),
                        value=arg.value
                    ))
                return cst.Dict(elements=elements)
        return updated_node

def main():
    with open("app.py", "r", encoding="utf-8") as f:
        code = f.read()

    module = cst.parse_module(code)
    transformer = DictToLiteralTransformer()
    new_module = module.visit(transformer)

    with open("app.py", "w", encoding="utf-8") as f:
        f.write(new_module.code)
    print("Replacement complete.")

if __name__ == "__main__":
    main()
