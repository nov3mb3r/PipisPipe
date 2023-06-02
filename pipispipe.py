from typing import List
from datetime import datetime
from volatility3.framework import renderers, interfaces, constants, exceptions
from volatility3.framework.configuration import requirements
from volatility3.plugins.windows import pslist, handles

class PipisPipe(interfaces.plugins.PluginInterface):
    """Enumerate Named Pipes for specified processes"""
    _required_framework_version = (1, 2, 0)
    _version = '1.0'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config.add_requirement(requirements.ListRequirement(name='pid_list',
                                                                  description='List of process IDs separated by space'))

    def _get_process_named_pipes(self, task: interfaces.objects.ObjectInterface) -> List[interfaces.objects.ObjectInterface]:
        """Return a list of named pipes for a given process"""
        handles_list = handles.Handles.list_handles(self.context, task)
        named_pipes_list = []

        for handle in handles_list:
            try:
                obj = handle.Object
                if obj.TypeName == '_FILE_OBJECT' and obj.get_object_type() == 'NamedPipe':
                    named_pipes_list.append(obj)
            except exceptions.PagedInvalidAddressException:
                pass

        return named_pipes_list

    def _get_processes_named_pipes(self, pid_list: List[int]) -> List[interfaces.objects.ObjectInterface]:
        """Return a list of named pipes for all processes in the pid_list"""
        processes_named_pipes = []
        for task in pslist.PsList.list_processes(self.context):
            if task.UniqueProcessId in pid_list:
                named_pipes_list = self._get_process_named_pipes(task)
                if named_pipes_list:
                    processes_named_pipes.append((task.ImageFileName.cast("string"), task.UniqueProcessId, named_pipes_list))

        return processes_named_pipes

    def run(self):
        pid_list = self._config.get('pid_list', default=None)
        if pid_list is None:
            raise ValueError('PID list not provided')

        # Convert input string of PIDs to a list of integers
        pid_list = [int(pid) for pid in pid_list.split()]

        processes_named_pipes = self._get_processes_named_pipes(pid_list)

        if not processes_named_pipes:
            return

        for proc_name, proc_pid, named_pipes_list in processes_named_pipes:
            rows = []
            for np in named_pipes_list:
                creation_time = np.CreationTime
                rows.append((str(np.FileName or '<unnamed>'), creation_time))
            # Sort the rows by creation time
            rows.sort(key=lambda x: x[1])

            yield (0, (proc_name, proc_pid), renderers.TreeGrid([("Pipe Name", str), ("Creation Time", datetime)] , sorted(rows, key=lambda x: x[1])))
