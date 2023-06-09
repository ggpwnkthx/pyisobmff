# File: libs/utils/isobmff/registries/__init__.py

import typing


class Registry:
    """
    Class responsible for managing the atom registry.

    Attributes:
    -----------
    __types : typing.Optional[typing.List[typing.Type]]
        The list of atom types to restrict to when registering.
    __registry : typing.Dict[str, typing.Type]
        A dictionary mapping atom types to their corresponding classes.
    """

    def __init__(self, types: typing.Optional[typing.List[typing.Type]]) -> None:
        """
        Initialize a new Registry object.

        Parameters:
        -----------
        types : typing.Optional[typing.List[typing.Type]], optional
            The list of atom types to restrict to when registering (default: None).
        """
        self.__types: typing.List[typing.Type] = types
        self.__registry: typing.Dict[str, typing.Type] = {}

    def __getitem__(self, atom_type: str) -> typing.Optional[typing.Type]:
        """
        Get the atom class corresponding to the provided atom type.

        Parameters:
        -----------
        atom_type : str
            The type of the atom.

        Returns:
        --------
        typing.Optional[typing.Type]
            The atom class corresponding to the provided atom type, or None if not found.
        """
        return self.__registry.get(
            atom_type, self.__registry.get("default", self.__types[0])
        )

    def __setitem__(self, name: str, _type: typing.Type) -> None:
        """
        Register a custom atom type and its corresponding class in the atom registry.

        Parameters:
        -----------
        name : str
            The name of the atom type to be registered.
        _type : typing.Type
            The class representing the atom.

        Raises:
        -------
        ValueError:
            If the atom type is already registered or the atom class doesn't inherit from the restricted types.

        Returns:
        --------
        None
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
        Check if the provided atom type is registered.

        Parameters:
        -----------
        name : str
            The name of the atom type.

        Returns:
        --------
        bool
            True if the atom type is registered, False otherwise.
        """
        return name in self.__registry
