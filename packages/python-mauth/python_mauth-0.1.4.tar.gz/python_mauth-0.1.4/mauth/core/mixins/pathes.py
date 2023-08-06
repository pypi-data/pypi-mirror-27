__all__ = (
    'PathMixin',
)


class PathMixin():
    """
    Mixin to define separate pathes for different REST methods.

    Attributes:
        path (str): Url path
    """
    path = ''

    def get_path(self, method: str, *args, **kwargs) -> str:
        """
        Returns path to process request for currect method.
        If there is no such path_variable, e.g. - `path_{method}`, uses
        `path`

        Args:
            method (str): Method, e.g. - create, update

        Returns:
            str: URL path to process request.
        """
        method_path = f'path_{method}'

        if hasattr(self, method_path):
            path = getattr(self, method_path, '')
        else:
            path = self.path

        return path.format(*args, **kwargs)
