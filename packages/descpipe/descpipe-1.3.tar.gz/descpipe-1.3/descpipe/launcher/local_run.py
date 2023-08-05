import os
from .. import utils
from .launcher import Launcher
from ..errors import InputError
import shutil

class LocalLauncher(Launcher):


    def run(self):
        self._check_inputs()
        utils.mkdir_p(self.data_dir())
        utils.mkdir_p(self.output_dir())

        for stage_name, stage_class in self.pipeline.sequence():
            self.run_stage(stage_name, stage_class)

        print("Pipeline complete. Extracting outputs.")

        for filename in os.listdir(self.data_dir()):
            path = os.path.join(self.data_dir(), filename)
            output_path = os.path.join(self.output_dir(), filename)
            os.replace(path, output_path)



    def working_dir(self):
        return self.info['working']        

    def data_dir(self):
        return os.path.join(self.working_dir(), "data")


    def _task_dirs(self, stage_name):
        stage_dir = os.path.join(self.working_dir(), stage_name)
        input_dir  = os.path.join(stage_dir, 'input')
        output_dir = os.path.join(stage_dir, 'output')
        config_dir = os.path.join(stage_dir, 'config')
        return input_dir, output_dir, config_dir

    def _input_path(self, input_tag, input_type):
        path = self.info['inputs'].get(input_tag)

        if path is None:
            path = os.path.join(self.data_dir(), input_tag+"."+input_type)

        return path

    def run_stage(self, stage_name, stage_class):
        print("Running pipeline stage: {}".format(stage_name))
        input_dir, output_dir, config_dir = self._task_dirs(stage_name)
        utils.mkdir_p(input_dir)
        utils.mkdir_p(output_dir)
        utils.mkdir_p(config_dir)
        utils.mkdir_p(self.output_dir())

        for config_tag, config_filename in stage_class.config.items():
            path = self.info['config'][stage_name][config_tag]
            task_path = os.path.join(config_dir, config_filename)
            print("Linking config file {} -> {}".format(path, task_path))
            utils.link_force(path, task_path)


        for input_tag, input_type in stage_class.inputs.items():
            path = self._input_path(input_tag, input_type)
            task_filename = "{}.{}".format(input_tag, input_type)
            task_path = os.path.join(input_dir, task_filename)
            print("Linking input file {} -> {}".format(path, task_path))
            utils.link_force(path, task_path)

        for output_tag, output_type  in stage_class.outputs.items():
            output_filename = "{}.{}".format(output_tag, output_type)

        image = self.pipeline.image_name(stage_name)
        input_mount = "-v {}:/opt/input".format(os.path.abspath(input_dir))
        output_mount = "-v {}:/opt/output".format(os.path.abspath(output_dir))
        config_mount = "-v {}:/opt/config".format(os.path.abspath(config_dir))

        cmd = "docker run --rm -it {} {} {} {} /opt/desc/run.py".format(
            input_mount, output_mount, config_mount, image)

        print("Running container:")
        print(cmd)
        status = os.system(cmd)

        if status != 0:
            raise RuntimeError("Pipeline failed at stage {}".format(stage_name))


        for output_tag, output_type  in stage_class.outputs.items():
            output_filename = "{}.{}".format(output_tag, output_type)
            task_path = os.path.join(output_dir, output_filename)
            data_path = os.path.join(self.data_dir(), output_filename)
            utils.link_force(task_path, data_path)


    def _check_inputs(self):
        inputs = self.pipeline.input_tags()
        for tag in inputs:
            path = self.info['inputs'].get(tag)
            if path is None:
                raise InputError("No path for input {} is specified in the pipeline file".format(tag))
            if not os.path.exists(path):
                raise InputError("Nothing found at specified input path: {}".format(path))
            if not os.path.isfile(path):
                raise InputError("Input path is a directory (not allowed): {}".format(path))


