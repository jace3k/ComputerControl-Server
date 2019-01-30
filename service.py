import logging as log

import command_pb2
import command_pb2_grpc
import functions


def setup_service(server, pin):
    log.debug('adding CommanderServicer to server')
    command_pb2_grpc.add_CommanderServicer_to_server(CommanderService(pin), server)


def sleep():
    functions.start_main_loop()


class CommanderService(command_pb2_grpc.CommanderServicer):
    def __init__(self, pin):
        self.pin = pin
        self.file_manager = functions.get_file_manager()

        functions.create_icon_tray(pin)
        functions.kl.start_key_listener()

    def pin_is_valid(self, metadata):
        return [True for x in metadata if x.key == 'pin' and x.value == self.pin]

    def LogIn(self, request, context):
        log.info('Running CommanderService.LogIn')
        if self.pin_is_valid(context.invocation_metadata()):
            functions.open_info_window('Użytkownik połączony', request.param, True)
            return command_pb2.Success(success=True)
        else:
            return command_pb2.Success(success=False)

    # INFO #################################################

    def GetStaticInfo(self, request, context):
        log.info('Running CommanderService.GetStaticInfo')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.StaticInfo(**functions.get_static_info())
        return command_pb2.StaticInfo()

    def GetFastIntervalInfo(self, request, context):
        log.info('Running CommanderService.GetFastIntervalInfo')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.FastIntervalInfo(**functions.get_fast_interval_info())
        return command_pb2.FastIntervalInfo()

    def GetSlowIntervalInfo(self, request, context):
        log.info('Running CommanderService.GetSlowIntervalInfo')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.SlowIntervalInfo(**functions.get_slow_interval_info())
        return command_pb2.SlowIntervalInfo()

    def GetShortInfo(self, request, context):
        log.info('Running CommanderService.GetShortInfo')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Welcome(**functions.get_short_info())
        return command_pb2.Welcome()

    def GetDiskInfo(self, request, context):
        log.info('Running CommanderService.GetDiskInfo')
        if self.pin_is_valid(context.invocation_metadata()):
            disk_info = command_pb2.DiskInfo()
            for disk in functions.get_disk_info():
                disk_proto = disk_info.disks.add()
                disk_proto.mountpoint = disk[0]
                disk_proto.fstype = disk[1]
                disk_proto.totalMemory = disk[2]
                disk_proto.usedMemory = disk[3]
                disk_proto.freeMemory = disk[4]
                disk_proto.percentMemory = disk[5]
            return disk_info
        return command_pb2.DiskInfo()

    # REGULATION ###########################################

    def SetVolume(self, request, context):
        log.info('Running CommanderService.SetVolume')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(**functions.set_volume(request.success))
        return command_pb2.Command(param=functions.INCORRECT_MSG)

    def SetBrightness(self, request, context):
        log.info('Running CommanderService.SetBrightness')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(**functions.set_brightness(request.value))
        return command_pb2.Command(param=functions.INCORRECT_MSG)

    # ON OFF ###############################################

    def Shutdown(self, request, context):
        log.info('Running CommanderService.Shutdown')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(**functions.shutdown(request.delay, request.restart, request.cancel))
        return command_pb2.Command(param=functions.INCORRECT_MSG)

    # FILE MANAGER #########################################

    def GetElementsInPath(self, request, context):
        log.info('Running CommanderService.GetElementsInPath')
        if self.pin_is_valid(context.invocation_metadata()):
            if request.param == '.':
                return self.build_elements_in_path()
            elif request.param == '..':
                self.file_manager.change_current_path('..')
                return self.build_elements_in_path()
            else:
                self.file_manager.change_current_path(request.param)
                return self.build_elements_in_path()
        return command_pb2.Elements()

    def build_elements_in_path(self):
        elements = command_pb2.Elements()
        elements.currentPath = self.file_manager.get_current_path()
        for item in self.file_manager.get_elements_in_path():
            element = elements.elementsInPath.add()
            element.name = item[0]
            element.type = item[1]
        return elements

    def OpenFile(self, request, context):
        log.info('Running CommanderService.OpenFile')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.File(**self.file_manager.open_file(request.param))
        return command_pb2.File()

    def DeleteFile(self, request, context):
        log.info('Running CommanderService.DeleteFile')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(**self.file_manager.delete_file(request.param))
        return command_pb2.Command(param=functions.INCORRECT_MSG)

    def CreateNewFolder(self, request, context):
        log.info('Running CommanderService.CreateNewFolder')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(**self.file_manager.create_new_folder(request.param))
        return command_pb2.Command(param=functions.INCORRECT_MSG)

    def SetBackground(self, request, context):
        log.info('Running CommanderService.SetBackground')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(**self.file_manager.set_background(request.param))
        return command_pb2.Command(param=functions.INCORRECT_MSG)

    # ADDITIONAL ###########################################

    def OpenCDROM(self, request, context):
        log.info('Running CommanderService.OpenCDROM')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(**functions.open_cd_rom())
        return command_pb2.Command(param=functions.INCORRECT_MSG)

    def OpenInternetBrowser(self, request, context):
        log.info('Running CommanderService.OpenInternetBrowser')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(**functions.open_internet_browser(request.param))
        return command_pb2.Command(param=functions.INCORRECT_MSG)

    def Screenshot(self, request, context):
        log.info('Running CommanderService.Screenshot')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.File(**functions.screenshot())
        return command_pb2.File()

    def GetKeyLogs(self, request, context):
        log.info('Running CommanderService.GetKeyLogs')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(**functions.get_key_logs())
        return command_pb2.Command(param=functions.INCORRECT_MSG)

    def OpenInfoWindow(self, request, context):
        log.info('Running CommanderService.OpenInfoWindow')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(
                **functions.open_info_window(request.text, request.title, request.isNotification))
        return command_pb2.Command(param=functions.INCORRECT_MSG)

    def Say(self, request, context):
        log.info('Running CommanderService.Say')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(**functions.say(request.param))
        return command_pb2.Command(param=functions.INCORRECT_MSG)

    def Click(self, request, context):
        log.info('Running CommanderService.ArrowClick')
        if self.pin_is_valid(context.invocation_metadata()):
            return command_pb2.Command(**functions.click(request.param))
        return command_pb2.Command(param=functions.INCORRECT_MSG)
