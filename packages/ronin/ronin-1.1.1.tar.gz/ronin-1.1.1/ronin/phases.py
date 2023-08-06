# -*- coding: utf-8 -*-
#
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

from .executors import Executor
from .extensions import Extension
from .contexts import current_context
from .utils.types import verify_type, verify_type_or_subclass
from .utils.paths import join_path, change_extension
from .utils.strings import stringify
from .utils.collections import StrictList, StrictDict
from .utils.compat import basestr
from types import FunctionType
from inspect import isclass
import os


class Phase(object):
    """
    A build phase within a project (see :class:`~ronin.projects.Project`).
    
    Each phase is equivalent to a single ``rule`` statement within a Ninja file together with the
    ``build`` statements that make use of it. Phases can be interrelated in complex ways: indeed,
    this feature is exactly what makes Rōnin useful (and writing Ninja files by hand difficult).
    
    Phases can work in either "multi-output" or "single-output" mode, the latter triggered by
    setting the ``output`` parameter. The former is often used for incremental compilation,
    the latter often used for linking various outputs to a single binary. 
    
    A phase must be set with a :class:`ronin.executors.Executor` to be useful. It was an
    architectural to separate the two classes in order to make it easier to extend code in each
    direction, however in the data model they are always joined.
    
    Another important part of the architecture is :class:`ronin.extensions.Extension`. This allows
    a kind of "live mix-in" for both phases and executors without having to extend those classes,
    for example to inject ``inputs`` and/or executor arguments.
    
    As a convenience, if you set the ``project`` and ``name`` init arguments, then the phase will
    automatically be added to that project. You can do this manually instead.

    :ivar vars: custom Ninja variables
    :vartype vars: {:obj:`basestring`: :obj:`~types.FunctionType` or :obj:`basestring`}
    :ivar hooks: called when generating the Ninja file
    :vartype hooks: [:obj:`~types.FunctionType`]
    """
    
    def __init__(self,
                 project=None,
                 name=None,
                 executor=None,
                 description=None,
                 inputs=None,
                 inputs_from=None,
                 input_path=None,
                 input_path_relative=None,
                 extensions=None,
                 output=None,
                 output_path=None,
                 output_path_relative=None,
                 output_strip_prefix=None,
                 output_strip_prefix_from=None,
                 output_transform=None,
                 run_output=False,
                 run_command=None,
                 rebuild_on=None,
                 rebuild_on_from=None,
                 build_if=None,
                 build_if_from=None):
        """
        :param project: project to which this phase will be added (if set must also set ``name``)
        :type project: ~ronin.projects.Project
        :param name: name in project to which this phase will be added (if set must also set
         ``project``)
        :type name: basestring or ~types.FunctionType
        :param executor: executor
        :type executor: ~ronin.executors.Executor
        :param description: Ninja description; may include Ninja variables, such as ``$out``;
         defaults to "[phase name] $out"
        :type description: basestring or ~types.FunctionType
        :param inputs: input paths; note that these should be *absolute* paths
        :type inputs: [:obj:`basestring` or :obj:`~types.FunctionType`]
        :param inputs_from: names or instances of other phases in the project, the outputs of which
         we add to this phase's ``inputs``
        :type inputs_from: [:obj:`basestring` or :obj:`~types.FunctionType` or :class:`Phase`]
        :param extensions: extensions
        :type extensions: ~ronin.extensions.Extension
        :param output: specifies that the phase has a *single* output; note that actual path of the
         output will be based on this parameter but not identical to it, for example "lib" might be
         added as a prefix, ".dll" as an extension, etc., according to the executor and/or project
         variant
        :type output: basestring or ~types.FunctionType
        :param output_path: override project's ``output_path``; otherwise will be based on the
         executor's ``output_type``
        :type output_path: basestring or ~types.FunctionType
        :param output_path_relative: joined to the context's ``paths.output``
        :type output_path_relative: basestring or ~types.FunctionType
        :param output_strip_prefix: stripped from outputs if they begin with this
        :type output_strip_prefix: basestring or ~types.FunctionType
        :param output_strip_prefix_from: name or instance of other phase in project, from which the
         output path is used as this phase's ``output_strip_prefix``
        :type output_strip_prefix_from: basestring or ~types.FunctionType or Phase
        :param output_transform: called on all outputs
        :type output_transform: ~types.FunctionType
        :param run_output: set to non-zero to run the output after a successful build in sequence
        :type  run_output: int
        :param run_command: arguments for the run command; use "{output}" to insert output 
        :type run_command: [:obj:`basestring` or :obj:`~types.FunctionType`]
        :param rebuild_on: similar to ``inputs`` but used as "implicit dependencies" in Ninja
         (single pipe), meaning that the ``build`` will be re-triggered when these files change
        :type rebuild_on: [:obj:`basestring` or :obj:`~types.FunctionType`]
        :param rebuild_on_from: names or instances of other phases in the project, the outputs of
         which we add to this phase's ``rebuild_on``
        :type rebuild_on_from: [:obj:`basestring` or :obj:`~types.FunctionType` or :class:`Phase`]
        :param build_if: similar to ``inputs`` but used as "order dependencies" in Ninja (double
         pipe), meaning that the ``build`` will be triggered only after these files are built
        :type build_if: [:obj:`basestring` or :obj:`~types.FunctionType`]
        :param build_if_from: names or instances of other phases in the project, the outputs of
         which we add to this phase's ``build_if``
        :type build_if_from: [:obj:`basestring` or :obj:`~types.FunctionType` or :class:`Phase`]
        """
        
        if project:
            verify_type(project, 'ronin.projects.Project')
            name = stringify(name)
            if name is None:
                raise ValueError('"name" cannot be None when "project" is specified')
            project.phases[name] = self
        if executor:
            verify_type(executor, Executor)
        if run_output and (not output):
            raise ValueError('"run_output" cannot be True or non-zero when "output" is None')
        if run_command and (not output):
            raise ValueError('"run_command" cannot be set when "output" is None')
        self.executor = executor
        self.description = description
        self.inputs = StrictList(inputs, value_type=(basestr, FunctionType))
        self.inputs_from = StrictList(inputs_from, value_type=(basestr, FunctionType,
                                                               'ronin.phases.Phase'))
        self.input_path = input_path
        self.input_path_relative = input_path_relative
        self.extensions = StrictList(extensions, value_type='ronin.extensions.Extension')
        self.output = output
        self.output_path = output_path
        self.output_path_relative = output_path_relative
        self.output_strip_prefix = output_strip_prefix
        self.output_strip_prefix_from = output_strip_prefix_from
        self.output_transform = output_transform
        self.run_output = run_output
        self.run_command = StrictList(run_command, value_type=(basestr, FunctionType))
        self.rebuild_on = StrictList(rebuild_on, value_type=(basestr, FunctionType))
        self.rebuild_on_from = StrictList(rebuild_on_from, value_type=(basestr, FunctionType,
                                                                       'ronin.phases.Phase'))
        self.build_if = StrictList(build_if, value_type=(basestr, FunctionType))
        self.build_if_from = StrictList(build_if_from, value_type=(basestr, FunctionType,
                                                                   'ronin.phases.Phase'))
        self.vars = StrictDict(key_type=basestr, value_type=(basestr, FunctionType))
        self.hooks = StrictList(value_type=FunctionType)

    def apply(self):
        """
        Applies all extensions and hooks to this phase.
        """
        
        def apply_extensions(extensions):
            for extension in extensions:
                verify_type_or_subclass(extension, Extension)
                if isclass(extension):
                    extension = extension()
                extension.apply_to_phase(self)
                apply_extensions(extension.extensions)

        apply_extensions(self.extensions)

        for hook in self.hooks:
            hook(self)

    def command_as_str(self, argument_filter=None):
        """
        Applies all extensions to the executor and calls its ``command_as_str``.
        
        :returns: command as string
        :rtype: basestring
        """
        
        def apply_extensions(extensions):
            for extension in extensions:
                verify_type_or_subclass(extension, Extension)
                if isclass(extension):
                    extension = extension()
                extension.apply_to_executor(self.executor)
                apply_extensions(extension.extensions)

        apply_extensions(self.extensions)

        return self.executor.command_as_str(argument_filter)

    @property
    def input_path(self):
        """
        The set ``input_path``, or the context's ``paths.input`` joined to ``input_path_relative``,
        or the project's ``input_path``.
        
        :type: :obj:`basestring`
        """
        
        input_path = stringify(self._input_path)
        if input_path is None:
            with current_context() as ctx:
                input_path_relative = stringify(self.input_path_relative)
                if input_path_relative is not None:
                    input_path = join_path(ctx.paths.input, input_path_relative)
                else:
                    input_path = ctx.current.project.input_path
        return input_path

    @input_path.setter
    def input_path(self, value):
        self._input_path = value

    @property
    def output_path(self):
        """
        The set ``output_path``, or the context's ``paths.output`` joined to
        ``output_path_relative``, or the project's ``output_path`` for the executor's
        ``output_type``.
        
        :type: :obj:`basestring`
        """

        output_path = stringify(self._output_path)
        if output_path is None:
            with current_context() as ctx:
                output_path_relative = stringify(self.output_path_relative)
                if output_path_relative is not None:
                    output_path = join_path(ctx.paths.output, output_path_relative)
                else:
                    output_path = ctx.current.project.get_output_path(self.executor.output_type)
        return output_path
    
    @output_path.setter
    def output_path(self, value):
        self._output_path = value

    def get_outputs(self, inputs):
        """
        Calculates the outputs for this phase depending on the inputs, applying output prefix and
        extension from the executor and finally the calling the ``output_transform`` function.
        
        :param inputs: inputs
        :type inputs: [:obj:`basestring`]
        :returns: (True if "single-output", outputs); length of ``outputs`` will always be 1 in
         "single-output" mode, otherwise it will be the same length as ``inputs``
        :rtype: (:obj:`bool`, [:class:`Output`])
        """
        
        # Paths
        input_path = self.input_path
        output_path = self.output_path

        # Filename changes
        output_extension = stringify(self.executor.output_extension)
        output_prefix = stringify(self.executor.output_prefix) or ''

        if self.output:
            # Combine all inputs into one output
            output = output_prefix + change_extension(self.output, output_extension)
            output = join_path(output_path, output)
            
            if self.output_transform:
                output = self.output_transform(output)
            
            if self.run_output:
                if self.run_command:
                    verify_type(self.run_command, list)
                    run_command = [stringify(v).format(output=output) for v in self.run_command]
                else:
                    run_command = [output]
                with current_context() as ctx:
                    ctx.current.project.run[self.run_output] = run_command
            
            return True, [Output(output_path, output)]
        elif inputs:
            # Each input matches an output
            
            # Strip prefix
            if self.output_strip_prefix_from:
                with current_context() as ctx:
                    _, p = ctx.current.project.get_phase_for(self.output_strip_prefix_from,
                                                             'output_strip_prefix_from')
                    if p:
                        output_strip_prefix = p.output_path
                    else:
                        output_strip_prefix = None
            else:
                output_strip_prefix = stringify(self.output_strip_prefix)
            if output_strip_prefix is None:
                output_strip_prefix = input_path
            if not output_strip_prefix.endswith(os.sep):
                output_strip_prefix += os.sep
            output_strip_prefix_length = len(output_strip_prefix)
    
            outputs = []            
            for the_input in inputs:
                output = the_input
                
                # Strip prefix
                if output.startswith(output_strip_prefix):
                    output = output[output_strip_prefix_length:]

                # Filename changes
                if output_prefix:
                    p, f = os.path.split(output)
                    output = join_path(p, output_prefix + f)
                output = change_extension(output, output_extension)
                
                output = join_path(output_path, output)

                if self.output_transform:
                    output = self.output_transform(output)

                outputs.append(Output(output_path, output))
                
            return False, outputs
        else:
            return False, []


class Output(object):
    """
    Phase output.
    """
    
    def __init__(self, path, the_file):
        """
        :param path: absolute path
        :type path: basestring
        :param the_file: file name
        :type the_file: basestring
        """
        
        self.path = path
        self.file = the_file
