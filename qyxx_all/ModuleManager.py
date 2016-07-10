# -*- coding: utf-8 -*-
# Created by David on 2016/5/4.

import sys
reload(sys)
sys.path.append('./util')
import copy
from util import common_util
from util.crawler_util import InputType,OutputParameterShowUpType,EventType,CrawlerRunMode,RetryFailedStrategy
from CommonLib.WebContent import WebAccessType, WebContent

class ModuleInput(object):
    '''
    模块输入参数封装
    '''
    def __init__(self, type, value, name=None, cache=False):
        self.type = type        # 参数类型，例如url、headers等
        self.value = value      # 参数值
        self.name = name        # 参数名称
        self.cache = cache      # 是否缓存该参数到value_dict

class ModuleOutput(object):
    '''
    模块输出参数封装
    '''
    def __init__(self, name, xpath, type, function, show_up, regex=None):
        self.name = name            # 输出参数的名称
        self.xpath = xpath          # 从页面内容提取参数使用的xpath
        self.regex = regex          # 从页面内容提取参数使用的regex
        self.type = type            # 输出参数的类型
        self.show_up = show_up      # 该输出是否必须出现
        self.function = function    # 输出参数时调用的方法

class Sleep(object):
    '''
    模块睡眠配置
    '''
    def __init__(self, seconds=2, condition=None):
        self.condition = condition
        self.seconds = seconds

class Event(object):
    '''
    模块事件配置
    '''
    def __init__(self,
                 event_type,
                 retry_times=2,
                 redo_module=None,
                 retry_failed_strategy=RetryFailedStrategy.EXIT,
                 assert_function=None):
        self.event_type = event_type                        # 事件类型
        self.retry_times = retry_times                      # 最大重试次数
        self.redo_module = redo_module                      # 重试模块
        self.retry_failed_strategy = retry_failed_strategy  # 所有重试均失败时的策略
        self.assert_function = assert_function              # 断言使用的方法
        self.isTriggered = False                            # 该事件是否已被触发

    def assertFunction(self, function):
        self.assert_function = function

class Iterator(object):
    '''
    迭代器，父模块用于遍历执行子模块
    '''
    def __init__(self, seeds, param_name):
        self.seeds = seeds              # 遍历使用的种子集合
        self.param_name = param_name    # 遍历中使用的变量名

class Adapter(object):
    '''
    适配器，用于对接上层模块的Router
    '''
    def __init__(self, kv_dict, name):
        self.kv_dict = kv_dict          # 适配成功所需的条件
        self.name = name                # 适配器名称

    def accept(self, value_dict):
        '''
        进行适配，以确定是否适配当前执行上下文
        :param value_dict: 当前变量上下文
        :return: 适配成功返回True，否则返回False
        '''
        if not self.kv_dict:
            return False
        info = u"根据"
        for key in self.kv_dict:
            if key not in value_dict:
                return False
            if self.kv_dict[key] != value_dict[key]:
                return False
            info += u"[%s=%s]," % (key, value_dict[key])
        print(info+u" 命中适配器 "+self.name)
        return True

class Router(object):
    '''
    提供路由服务，与下级模块中的Adapter对接
    '''
    def __init__(self):
        self.modules = None   # 持有的不同路径的模块

    def appendSubModule(self, module):
        if not self.modules:
            self.modules = list()
        self.modules.append(module)

    def route(self, value_dict):
        '''
        选择下级需要执行的模块
        :param value_dict:
        :return: 若某个模块适配成功，则返回该模块
        '''
        for module in self.modules:
            if not module.adapter:
                continue
            if module.adapter.accept(value_dict):
                return module
        return None

class Bypass(object):
    '''
    Bypass is used to bypass some modules under specific condition
    '''
    def __init__(self, condition_fuc, module_id=None, jump_to_module=None, range_global=False):
        self.module_id = module_id                  # the module should be bypassed
        self.jump_to_module = jump_to_module        # which module should jump to, it's priority is higher than modules
        self.condition_func = condition_fuc         # the condition function
        self.range_global = range_global            # the effective range, can be global or not
        self.activated = False                      # whether this bypass is activated

class Module(object):
    '''
    模块类，爬虫执行中一个独立运行单元
    '''
    def __init__(self, function=None, name=None, iterator=None, router=None):
        self.module_id = None               # 模块id，通常用于跳转中识别跳转模块
        self.function = function            # 当前模块对应的模块方法
        self.name = name                    # 当前模块名称，通常用于log输出
        self.inputs = list()                # 当前模块的输入参数集合
        self.outputs = list()               # 当前模块的输出参数集合
        self.use_proxy = True               # 当前模块是否使用代理
        self.extra_functions = None         # 子类需执行的个性方法，例如打印输出监视变量的值
        self.monitor_values = None          # 需要监视的变量
        self.modules = None                 # 当前模块持有的子模块
        self.iterator = iterator            # 迭代器，当前模块需遍历调用各个子模块时使用
        self.next_module = None             # 下级模块
        self.mapper_config = None           # 映射配置，用于结果集的映射
        self.module_manager = None          # 持有对模块管理器的引用，方便查找跳转模块
        self.router = router                # 路由器
        self.adapter = None                 # 适配器
        self.web_content = None             # 当前模块需要解读的web内容，用于web内容直接来自上级模块处理而非网络
        self.bypasses = None                # 需要动态跳过的模块
        # 以下为运行时会动态变化的属性
        self.sleep = Sleep()                # 当前模块的休眠配置
        self.events = None                  # 当前模块支持的事件
        self.run_state = EventType.NORMAL   # 当前模块运行结果状态
        self.redo_times = 0                 # 当前模块已重做次数
        self.snapshot_dict = dict()         # 保存之前状态

    def snapshot(self):
        """
        snapshot the status before changed
        :return:
        """
        self.snapshot_dict['sleep'] = copy.deepcopy(self.sleep)
        self.snapshot_dict['events'] = copy.deepcopy(self.events)
        self.snapshot_dict['run_state'] = copy.deepcopy(self.run_state)
        self.snapshot_dict['redo_times'] = copy.deepcopy(self.redo_times)

    def recoverFromSnapshot(self):
        """
        recover the status from the previous status
        :return:
        """
        if not self.snapshot_dict:
            return
        self.sleep = copy.deepcopy(self.snapshot_dict['sleep'])
        self.events = copy.deepcopy(self.snapshot_dict['events'])
        self.run_state = copy.deepcopy(self.snapshot_dict['run_state'])
        self.redo_times = copy.deepcopy(self.snapshot_dict['redo_times'])

    def appendInput(self, input_type, input_value, input_name=None):
        """
        append an input parameter to current module
        :param input_type: the input type, can be url,headers etc.
        :param input_value: the input value, can be straight string or a key in value_dict
        :param input_name: the name of the input
        :return:
        """
        self.inputs.append(ModuleInput(input_type, input_value, input_name))
        pass

    def appendOutput(self, name=None, xpath=None, type=None, function=None, show_up=OutputParameterShowUpType.MUST, regex=None):
        """
        append an output parameter to current module
        :param name:
        :param xpath:
        :param type:
        :param function:
        :param show_up:
        :return:
        """
        self.outputs.append(ModuleOutput(name, xpath, type, function, show_up, regex))

    def appendExtraFunction(self, function):
        """
        append extra functions for current module
        :param function:
        :return:
        """
        if not self.extra_functions:
            self.extra_functions = list()
        if function:
            self.extra_functions.append(function)

    def appendMiddleValueMonitor(self, *middle_values):
        """
        append middle value that you want to monitor
        :param middle_value:
        :return:
        """
        if not middle_values:
            return
        if not self.monitor_values:
            self.monitor_values = list()
        self.monitor_values.extend(middle_values)

    def appendUrl(self, input_value):
        """
        append an url directly
        :param input_value:
        :return:
        """
        self.appendInput(InputType.URL, input_value)

    def appendHeaders(self, input_value):
        """
        append the headers directly
        :param input_value:
        :return:
        """
        self.appendInput(InputType.HEADERS, input_value)

    def appendWebMethod(self, input_value):
        """
        append the web method directly
        :param input_value:
        :return:
        """
        self.appendInput(InputType.METHOD, input_value)

    def appendPostData(self, input_value):
        """
        append the post data directly
        :param input_value:
        :return:
        """
        self.appendInput(InputType.POST_DATA, input_value)

    def appendEncoding(self, input_value):
        """
        specify the encoding for the web page content
        :param input_value:
        :return:
        """
        self.appendInput(InputType.ENCODING, input_value)

    def appendCookie(self, input_value):
        """
        append the cookie directly
        :param input_value:
        :return:
        """
        self.appendInput(InputType.COOKIE, input_value)

    def appendAcceptCode(self, status_code):
        """
        append the accept code for the current module
        :param status_code:
        :return:
        """
        self.appendInput(InputType.STATUS_CODE, status_code)

    def appendWebContent(self, input_value):
        """
        set the content directly, not through the network
        :param input_value:
        :return:
        """
        if not input_value:
            return
        self.web_content = input_value

    def repalceInput(self, input_type, input_value, input_name=None):
        """
        replace the input value with the new value
        :param input_type: the type you need to replace
        :param input_value: the new value you want to set
        :return:
        """
        input = ModuleInput(input_type, input_value, input_name)
        tmp_list = list(self.inputs)
        for it in tmp_list:
            if it.type == input_type:
                self.inputs.remove(it)
        self.inputs.append(input)

    def appendBypass(self, bypass):
        """
        append a bypass into the current module
        :param bypass:
        :return:
        """
        if not self.bypasses:
            self.bypasses = list()
        self.bypasses.append(bypass)
        if bypass.range_global:
            self.module_manager.registerBypass(bypass)

    def addMapper(self, map_dict):
        """
        add the map config for result map
        :param map_dict:
        :return:
        """
        self.mapper_config = map_dict

    def addSleep(self, sleep):
        """
        add a sleep object for controlling the sleep time and condition
        :param sleep:
        :return:
        """
        self.sleep = sleep

    def addRouter(self, router):
        '''
        添加路由器，路由器中持有的各个模块为并行存储，不同于默认链式存储
        因此，不同先添加子模块，后添加router
        :param router:
        :return:
        '''
        if self.modules:
            raise Exception("非法操作！不能先添加module，后添加router！")
        self.router = router

    def addAdapter(self, adapter):
        """
        add an adapter for docking with the router
        :param adapter:
        :return:
        """
        self.adapter = adapter

    def addEvent(self, event):
        """
        add an event for current module
        :param event:
        :return:
        """
        if not event:
            return
        if not self.events:
            self.events = dict()
        if event.event_type not in self.events:
            self.events[event.event_type] = list()
        self.events[event.event_type].append(event)

    def setProxy(self, use_proxy):
        """
        set a bool value to point whether current module use proxy
        :param use_proxy:
        :return:
        """
        if use_proxy is None:
            return
        self.use_proxy = use_proxy

    def eventExist(self, event_type):
        """
        whether an event is exist
        :param event_type:
        :return:
        """
        if not self.events:
            return False
        return event_type in self.events

    def detectWebContent(self, web, redo_module=None, log=None):
        """
        检测页面内容返回情况，并动态添加和触发对应事件
        :param web:
        :param redo_module:
        :param log:
        :return:
        """
        if web and web.access_type == WebAccessType.OK:
            self.run_state = EventType.NORMAL
            return
        if not self.eventExist(EventType.WEB_CONTENT_FAILED) or not self.events[EventType.WEB_CONTENT_FAILED]:
            self.snapshot()
            event = Event(EventType.WEB_CONTENT_FAILED, retry_times=10, redo_module=redo_module)
            self.addEvent(event)
        else:
            event = self.events[EventType.WEB_CONTENT_FAILED][0]
        event.isTriggered = True
        self.run_state = EventType.WEB_CONTENT_FAILED
        self.sleep.seconds += 1
        if log:
            log.info("为当前模块增加睡眠时间1秒，调整后为 %s 秒" % self.sleep.seconds)

    def supportDefaultEvent(self):
        """
        支持默认事件处理：异常和未得到期望输出
        :return:
        """
        if self.events:
            return
        self.events = dict()
        self.events[EventType.EXCEPTION_OCCURED] = list()
        self.events[EventType.EXCEPTION_OCCURED].append(Event(EventType.EXCEPTION_OCCURED))
        self.events[EventType.OUTPUT_NOT_SATISFIED] = list()
        self.events[EventType.OUTPUT_NOT_SATISFIED].append(Event(EventType.OUTPUT_NOT_SATISFIED))

    def appendSubModule(self, module, supportDefaultEvent=False):
        '''
        添加子模块，默认为链式存储
        :param module: 待添加的子模块
        :param supportDefaultEvent:是否支持默认事件
        :return:
        '''
        if supportDefaultEvent:
            module.supportDefaultEvent()
        if self.router:
            self.router.appendSubModule(module)
            return
        if not self.modules:
            self.modules = list()
        else:
            self.modules[-1].next_module = module
        self.modules.append(module)
        self.module_manager.register(module)
        module.module_manager = self.module_manager

    def canIterate(self):
        """
        whether the current module can be iterate
        :return:
        """
        return self.iterator and self.modules and len(self.modules) > 0

    def hasSubModules(self):
        """
        whether the current module has sub modules
        :return:
        """
        return self.modules and len(self.modules) > 0

    def outputsDescription(self):
        """
        describe the outputs of the current module
        :return:
        """
        if not self.outputs:
            return ''
        description = ''
        for output in self.outputs:
            if not output.name:
                continue
            description += output.name+","
        return description

    def getInputValue(self, input, value_dict, log=None):
        """
        get the value of current module:
        1.find the value from value_dict
        2.compute the value with function
        3.the literal value
        :param input:
        :param value_dict:
        :param log:
        :return:
        """
        if not input.value:
            return None
        if isinstance(input.value, basestring) and input.value in value_dict:
            value = value_dict[input.value]
        elif common_util.is_function(input.value):
            value = common_util.run_function(input.value, value_dict, log)
        else:
            value = input.value
        # 缓存输入结果，例如北京基本信息url
        if input.cache:
            value_dict[input.name] = value
        return value

    def getInputByType(self, type, value_dict, log=None):
        """
        get the input value by type
        :param type:
        :param value_dict:
        :param log:
        :return:
        """
        if not self.inputs:
            return None
        for input in self.inputs:
            if input.type == type:
                value = self.getInputValue(input, value_dict, log)
                return value

    def getHttpInput(self, value_dict, log=None):
        """
        get the basic input values for accessing web
        :param value_dict:
        :param log:
        :return:
        """
        url = None
        headers = None
        method = None
        post_data = None
        if not self.inputs:
            return url, headers, method, post_data
        for input in self.inputs:
            if input.type == InputType.URL:
                url = self.getInputValue(input, value_dict, log)
            elif input.type == InputType.HEADERS:
                headers = self.getInputValue(input, value_dict, log)
            elif input.type == InputType.METHOD:
                method = self.getInputValue(input, value_dict, log)
            elif input.type == InputType.POST_DATA:
                post_data = self.getInputValue(input, value_dict, log)

        if not method:
            method = "get"

        return url, headers, method, post_data

    def triggerEvent(self, event_type, event=None):
        """
        触发事件
        :param event_type:需要触发的事件类型
        :param event: 为空时会触发一组对应类型的事件
        :return:
        """
        if not self.events or event_type not in self.events:
            return
        if event and event in self.events[event_type]:
            event.isTriggered = True
            return
        for event in self.events[event_type]:
            if event.isTriggered:
                return
        for event in self.events[event_type]:
            event.isTriggered = True

    def untriggerEvent(self):
        """
        触发事件
        :param event_type:需要触发的事件类型
        :param event: 为空时会触发一组对应类型的事件
        :return:
        """
        if not self.events:
            return
        for etype in self.events:
            for event in self.events[etype]:
                event.isTriggered = False

    def getRedoModule(self, redo_module_id):
        """
        get the redo module by the redo module id
        :param redo_module_id:
        :return:
        """
        self.redo_times += 1
        if not redo_module_id:
            return self
        module = self.module_manager.getModule(redo_module_id)
        if not module:
            return self
        return module

    def getNextModule(self, value_dict):
        """
        get the next module of current module
        :param value_dict:
        :return:
        """
        if self.router:
            return self.router.route(value_dict)
        next_module = self.next_module
        if not next_module:
            return next_module
        if self.bypasses:
            # 处理需要绕过的模块
            bypass_modules = list()
            for bp in self.bypasses:
                if not bp:
                    continue
                if bp.condition_func and common_util.is_function(bp.condition_func):
                    bp.activated = common_util.run_function(bp.condition_func, value_dict)
                    if bp.activated:
                        if bp.jump_to_module:
                            module = self.module_manager.getModule(bp.jump_to_module)
                            if module:
                                return module
                        bypass_modules.append(bp.module_id)
            while next_module and next_module.module_id and next_module.module_id in bypass_modules:
                next_module = next_module.next_module
        # 处理全局bypass
        if not next_module:
            return next_module
        maybe_bypassed = self.module_manager.getBypass(next_module.module_id)
        while next_module.module_id and maybe_bypassed:
            satisfied = False
            for bp in maybe_bypassed:
                if bp.activated:
                    next_module = next_module.next_module
                    if not next_module:
                        return next_module
                    maybe_bypassed = self.module_manager.getBypass(next_module.module_id)
                    satisfied = True
                    break
            if not satisfied:
                break
        return next_module

class ModuleManager(object):
    """
    ModuleManager is used to manage the modules
    """
    def __init__(self):
        """
        Initial all the fields
        """
        self.mode = None
        self.modules = None
        self.module_dict = dict()
        self.module_register = dict()
        self.bypass_register = dict()

    def switchToMode(self, run_mode):
        """
        switch to a specific mode for crawling
        :param run_mode:
        :return:
        """
        self.mode = run_mode
        if self.mode not in self.module_dict:
            self.module_dict[self.mode] = list()
        self.modules = self.module_dict[self.mode]

    def appendSubModule(self, module, supportDefaultEvent=False):
        """
        append one module to the module manager
        :param module:
        :param supportDefaultEvent: whether support the default events
        :return:
        """
        if supportDefaultEvent:
            module.supportDefaultEvent()
        if self.modules:
            self.modules[-1].next_module = module
        self.modules.append(module)
        self.initialized = True
        self.register(module)
        module.module_manager = self

    def register(self, module):
        """
        register one module into dict
        :param module:
        :return:
        """
        if module.module_id:
            self.module_register[module.module_id] = module

    def registerBypass(self, bypass):
        """
        register the global bypass
        :param module:
        :return:
        """
        if not bypass.range_global:
            return
        if not bypass.module_id:
            return
        if bypass.module_id not in self.bypass_register:
            self.bypass_register[bypass.module_id] = list()
        self.bypass_register[bypass.module_id].append(bypass)

    def getBypass(self, module_id):
        """
        whether the module_id in the global bypass modules
        :param module_id:
        :return:
        """
        if module_id and module_id in self.bypass_register:
            return self.bypass_register[module_id]
        return None

    def getModule(self, module_id):
        """
        get a module by id
        :param module_id:
        :return:
        """
        if module_id in self.module_register:
            return self.module_register[module_id]
        return None

    def getFirstModule(self):
        """
        get the first module of the manager
        :return:
        """
        # 若modules为空，可能是适配器模式下外部未主动调用switch，默认先将模式切换至adapter模式
        if not self.modules:
            self.switchToMode(CrawlerRunMode.COMPANY_ADAPTER)
        if not self.modules:
            return None
        return self.modules[0]

    def isFirstModule(self, module):
        """
        whether it is the first module
        :param module:
        :return:
        """
        if not module:
            return False
        if not self.modules:
            self.switchToMode(CrawlerRunMode.COMPANY_ADAPTER)
        if not self.modules:
            return False
        return self.modules[0] == module


'''
中间结果集约定：
1.验证码输出 yzm
2.页面输出页面内容及web对象 html,web
3.json输出页面内容及web对象 json,web
4.股东信息表头表值键值对 gdxx_list
5.待搜索公司关键字 company_key
6.搜索列表中的每一个公司名 search_company
7.公司信息中间抓取结果以键值company存放在result_dict和value_dict
8.待搜索公司的company_url

事件判定优先级次序：
1.异常事件
2.断言失败事件
3.web页面内容访问异常，如被反爬
4.未得到期望输出事件

rowkey的支持：

'''
if __name__ == "__main__":
    # cb = CrawlerBeijing("beijing")
    # common_util.run_function(cb.test, None)
    pass



