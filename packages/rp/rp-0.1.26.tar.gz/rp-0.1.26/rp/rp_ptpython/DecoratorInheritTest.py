def inherit_def(parent,child=None):
    if child is None:
        return lambda z:inherit_def(parent,z)
    # Author: Ryan Burgert
    # This decorator modifies the child in-place without copying it!
    # Made because I don't like creating classes when it can be avoided; I'd much rather crate new functions.
    # This is a decorator used to override default method inputs.
    assert callable(child )
    assert callable(parent)
    #
    import inspect as inspect
    child_spec =inspect.getfullargspec(child )
    parent_spec=inspect.getfullargspec(parent)
    #region  Example of getfullargspec results:
        #      ⎧                                    ⎫
        # def f(a, b:str, c=0, d:int=1, *e, f=2, **g):pass
        #      ⎩                                    ⎭
        #             ⎧                                                                                                                                                                   ⎫
        #             ⎪     ⎧                  ⎫                                   ⎧    ⎫             ⎧   ⎫                 ⎧      ⎫              ⎧                                      ⎫⎪
        #  FullArgSpec(args=['a', 'b', 'c', 'd'], varargs='e', varkw='g', defaults=(0, 1), kwonlyargs=['f'], kwonlydefaults={'f': 2}, annotations={'b': <class 'str'>, 'd': <class 'int'>})
        #             ⎪     ⎩                  ⎭                                   ⎩    ⎭             ⎩   ⎭                 ⎩      ⎭              ⎩                                      ⎭⎪
        #             ⎩                                                                                                                                                                   ⎭
    #endregion
    child_args            =child_spec .args

    from rp import mini_terminal_for_pythonista
    exec(mini_terminal_for_pythonista)

    parent_defaults=parent_spec.defaults or []
    child_defaults=child_spec.defaults or []
    undefaulted_child_args=child_args [:len(child_defaults)]
    parent_args           =parent_spec.args or []
    defaulted_parent_args =parent_args[-len(parent_defaults):]
    #
    parent_defaults=dict(zip(parent_args,parent_defaults))# parent_spec.defaults ≣ parent.__defaults__
    parent_defaults.update(parent.__kwdefaults__ or {})# Should be no overrides
    #
    flag=True
    for arg,default in reversed(undefaulted_child_args):# All un-defaulted child args
        if arg in parent_defaults:
            assert flag,'Error: Please rearrange arguments, this is a vague error message (that could easily be improved) but you cant extend functions like that'
            # Assertion Explanation:
            # NOTE: All default args MUST come before undefaulted args, by rules of python syntax.
            #     def parent(a=5):pass
            #     def child(z,a,x):pass
            #   First possiblity for handling this: x is None, and no longer required (which modifies the child)
            #     def child(z,a=5,x=None):pass
            #   Second possiblity for handling this: (reordering arguments; could be REALLY hard to debug if misused, which might be easy to do)
            #     def child(z,x,a=5):pass
            # This method should use neither method for handling it and instead just throw an error.
            child.__defaults__=(parent_defaults[arg],)+child.__defaults__
        else:
            flag=False
    from rp import merge_dicts
    for key in set(parent.__kwdefaults__ or {})-set(child.__defaults__ or {})-set(parent_args)-set(child_args):
        child.__kwdefaults__=[key]=parent.__kwdefaults__[key]
    #
    return child


def f(a=4):
    print(a)
f(4)
@inherit_def(f)
def g(x):
    print(a)
g(42)