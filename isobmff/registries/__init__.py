# File: isobmff/registries/__init__.py

import typing


class Registry:
    """
    Class responsible for managing a registry.

    Attributes:
    -----------
    __types : typing.Optional[typing.List[typing.Type]]
        The list of types to restrict to when registering.
    __registry : typing.Dict[str, typing.Type]
        A dictionary mapping types to their corresponding classes.

    Notes:
    ------
    - The `Registry` class provides a central registry for managing types and their corresponding classes.
    - It allows registering custom types and their classes and provides a way to retrieve the class for a given type.
    - The registry supports restricting the registered classes to a specific list of types if desired.
    """

    def __init__(self, types: typing.Optional[typing.List[typing.Type]]) -> None:
        """
        Initialize a new Registry object.

        Parameters:
        -----------
        types : typing.Optional[typing.List[typing.Type]], optional
            The list of types to restrict to when registering (default: None).

        Notes:
        ------
        - The `types` parameter allows specifying a list of types to restrict the registry to.
        - Only classes that inherit from the restricted types can be registered.
        """
        self.__types: typing.List[typing.Type] = types
        self.__registry: typing.Dict[str, typing.Type] = {}

    def __getitem__(self, _type: str) -> typing.Optional[typing.Type]:
        """
        Get the class corresponding to the provided type.

        Parameters:
        -----------
        _type : str
            The type of the object.

        Returns:
        --------
        typing.Optional[typing.Type]
            The class corresponding to the provided type, or None if not found.

        Notes:
        ------
        - If the type is not found in the registry, it falls back to a default class if available.
        """
        return self.__registry.get(
            _type, self.__registry.get("default", self.__types[0])
        )

    def __setitem__(self, name: str, _type: typing.Type) -> None:
        """
        Register a custom type and its corresponding class in the registry.

        Parameters:
        -----------
        name : str
            The name of the type to be registered.
        _type : typing.Type
            The class representing the object.

        Raises:
        -------
        ValueError:
            If the type is already registered or the class doesn't inherit from the restricted types.

        Returns:
        --------
        None
        
        Notes:
        ------
        - Only classes that inherit from the restricted types can be registered.
        - If the type is already registered, a `ValueError` is raised.
        """
        if not (callable(_type) and typing.Callable in self.__types):
            if self.__types and not any(issubclass(_type, t) for t in self.__types):
                raise ValueError(
                    f"Class must be a subclass of {', '.join(t.__name__ for t in self.__types)}"
                )
        if name in self.__registry:
            raise ValueError(f"Class name '{name}' is already registered.")
        self.__registry[name] = _type

    def __contains__(self, name: str) -> bool:
        """
        Check if the provided type is registered.

        Parameters:
        -----------
        name : str
            The name of the type.

        Returns:
        --------
        bool
            True if the type is registered, False otherwise.

        Notes:
        ------
        - This method allows checking if a given type is registered in the registry.
        """
        return name in self.__registry
