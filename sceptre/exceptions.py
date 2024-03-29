# -*- coding: utf-8 -*-


class SceptreException(Exception):
    """
    Base class for all Sceptre errors
    """
    pass


class ProjectAlreadyExistsError(SceptreException):
    """
    Error raised when Sceptre project already exists.
    """
    pass


class InvalidSceptreDirectoryError(SceptreException):
    """
    Error raised if a sceptre directory is invalid.
    """
    pass


class UnsupportedTemplateFileTypeError(SceptreException):
    """
    Error raised if an unsupported template file type is used.
    """
    pass


class TemplateSceptreHandlerError(SceptreException):
    """
    Error raised if sceptre_handler() is not defined correctly in the template.
    """
    pass


class DependencyStackNotLaunchedError(SceptreException):
    """
    Error raised when a dependency stack has not been launched
    """
    pass


class DependencyStackMissingOutputError(SceptreException):
    """
    Error raised if a dependency stack does not have the correct outputs.
    """
    pass


class CircularDependenciesError(SceptreException):
    """
    Error raised if there are circular dependencies
    """
    pass


class UnknownStackStatusError(SceptreException):
    """
    Error raised if an unknown stack status is received.
    """
    pass


class RetryLimitExceededError(SceptreException):
    """
    Error raised if the request limit is exceeded.
    """
    pass


class UnknownHookTypeError(SceptreException):
    """
    Error raised if an unrecognised hook type is received.
    """


class VersionIncompatibleError(SceptreException):
    """
    Error raised if configuration incompatible with running version.
    """
    pass


class ProtectedStackError(SceptreException):
    """
    Error raised upon execution of an action under active protection
    """
    pass


class UnknownStackChangeSetStatusError(SceptreException):
    """
    Error raised if an unknown stack change set status is received.
    """
    pass


class InvalidHookArgumentTypeError(SceptreException):
    """
    Error raised if a hook's argument type is invalid.
    """
    pass


class InvalidHookArgumentSyntaxError(SceptreException):
    """
    Error raised if a hook's argument syntax is invalid.
    """
    pass


class InvalidHookArgumentValueError(SceptreException):
    """
    Error raised if a hook's argument value is invalid.
    """
    pass


class CannotUpdateFailedStackError(SceptreException):
    """
    Error raised when a failed stack is updated.
    """
    pass


class StackDoesNotExistError(SceptreException):
    """
    Error raised when a stack does not exist.
    """
    pass


class ConfigFileNotFoundError(SceptreException):
    """
    Error raised when a config file does not exist.
    """
    pass


class InvalidConfigFileError(SceptreException):
    """
    Error raised when a config file lacks mandatory keys.
    """
    pass


class PathConversionError(SceptreException):
    """
    Error raised when a path is unable to be converted.
    """
    pass


class InvalidProviderCredentialsError(SceptreException):
    """
    Error raised when Provider credentials are invalid.
    """
    pass


class ClientError(SceptreException):
    """
    Error raised when connecting to a Provider Client
    """
    pass


class InvalidProviderSchemaError(SceptreException):
    """
    Error raised when a ProviderSchema does not have required keys.
    """
    pass


class SceptreYamlError(SceptreException):
    """
    Error raised when a SceptreYamlParser cannot parse a file stream correctly.
    """
    pass


class DuplicateProviderRegistrationError(SceptreException):
    """
    Error raised when two Providers attempt to register themselves on the
    ProviderRegistry with the same registry_key.
    """
    pass


class ProviderNotFoundError(SceptreException):
    """
    Error raised when attempting to access a Provider that is not in the ProviderRegsitry.
    """
    pass
