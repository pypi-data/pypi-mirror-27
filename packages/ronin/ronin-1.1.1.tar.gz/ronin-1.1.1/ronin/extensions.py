# Copyright 2016-2018 Tal Liron
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .contexts import current_context
from .utils.types import verify_type
from .utils.collections import StrictList
from .utils.compat import basestr
from .utils.strings import stringify
from types import FunctionType


class Extension(object):
    """
    Base class for extensions.
    
    Extensions can nest child extensions (and so can they).
    
    :ivar extensions: child extensions
    :vartype command: [:class:`Extension`]
    """
    
    def __init__(self):
        self.extensions = StrictList(value_type=Extension)

    def apply_to_phase(self, phase):
        pass
    
    def apply_to_executor(self, executor):
        for command_type in executor.command_types:
            fn = getattr(self, 'apply_to_executor_{}'.format(command_type), None)
            if fn:
                fn(executor)


class ExplicitExtension(Extension):
    """
    An extension with explicitly stated data to support gcc-like executors.
    """
    
    def __init__(self, inputs=None, include_paths=None, defines=None, library_paths=None,
                 libraries=None):
        """
        :param inputs: input paths; note that these should be *absolute* paths
        :type inputs: [:obj:`basestring` or :obj:`~types.FunctionType`]
        :param include_paths: include paths; note that these should be *absolute* paths
        :type include_paths: [:obj:`basestring` or :obj:`~types.FunctionType`]
        :param defines: defines in a (name, value) tuple format; use None for value if the define
         does not have a value
        :type defines: [(:obj:`basestring` or :obj:`~types.FunctionType`, :obj:`basestring` or
         :obj:`~types.FunctionType`)]
        :param library_paths: include paths; note that these should be *absolute* paths
        :type library_paths: [:obj:`basestring` or :obj:`~types.FunctionType`]
        :param libraries: library names
        :type libraries: [:obj:`basestring` or :obj:`~types.FunctionType`]
        """
        
        super(ExplicitExtension, self).__init__()
        self.inputs = StrictList(inputs, value_type=(basestr, FunctionType))
        self.include_paths = StrictList(include_paths, value_type=(basestr, FunctionType))
        self.defines = defines or []
        self.library_paths = StrictList(library_paths, value_type=(basestr, FunctionType))
        self.libraries = StrictList(libraries, value_type=(basestr, FunctionType))

    def apply_to_phase(self, phase):
        phase.inputs += self.inputs

    def apply_to_executor_gcc_compile(self, executor):
        for path in self.include_paths:
            executor.add_include_path(path)
        for define, value in self.defines:
            executor.define(define, value)

    def apply_to_executor_gcc_link(self, executor):
        for path in self.library_paths:
            executor.add_library_path(path)
        for library in self.libraries:
            executor.add_library(library)


class OutputsExtension(Extension):
    """
    An extension that pulls in outputs from another build phase.
    """
    
    def __init__(self, project, phase_name):
        """
        :param project: project
        :type project: ~ronin.projects.Project
        :param phase_name: phase name in project
        :type phase_name: basestring or ~types.FunctionType
        """
        
        super(OutputsExtension, self).__init__()
        verify_type(project, 'ronin.projects.Project')
        self._project = project
        self._phase_name = phase_name
    
    def apply_to_executor_gcc_link(self, executor):
        with current_context() as ctx:
            project_outputs = ctx.get('current.project_outputs')
        if project_outputs is None:
            return
        phase_outputs = project_outputs.get(self._project)
        if phase_outputs is None:
            return
        outputs = phase_outputs.get(stringify(self._phase_name))
        if outputs is None:
            return
        for output in outputs:
            executor.add_input(output.file)
