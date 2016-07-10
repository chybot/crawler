# -*- coding: utf-8 -*-
# Created by David on 2016/4/14.

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import time
import uuid
sys.path.append("../")
sys.path.append("util/")
from CommonLib import exceptutil
import util.common_util as util
from util.HolderUtil import HolderUtil
from util.crawler_util import InputType,OutputParameterShowUpType
from util.crawler_util import OutputType,EventType,RetryFailedStrategy
from CrawlerTrace import CrawlerTrace


class CrawlerControl:
    '''
    爬虫通用控制流程框架，通过配置文件+动态调用实现模块的执行控制
    '''
    def __init__(self, crawler):
        '''
        初始化方法
        :param pinyin: 省份的拼音，需要与配置文件crawler_base_config.crawlers中的配置对应
        :param type: 例如“北京企业”，北京爬虫舶来品，目前尚未完全明了含义
        '''
        self.crawler = crawler
        self.holder = crawler.holder
        self.init()

    def init(self):
        '''
        每爬取一次种子会被初始化一次
        :return:
        '''
        self.trace = CrawlerTrace()

    def crawl(self):
        '''
        根据传入的配置文件和公司关键字、公司名执行抓取
        :param config_file:格式示例 D:\SVN\qyxx_all_in_one\crawler_beijing_config
        :return:
        '''
        try:
            self.init()

            module = self.crawler.module_manager.getFirstModule()

            self.snapFirstModuleForRedo(module)

            self.run_module_chain(module)

            self.holder.logging.info(self.trace.description())

        except Exception as e:
            self.error_handler(e)

    def run_module_chain(self, module):
        '''
        负责整体爬虫调度，根据crawler的反馈，决定下一步爬取的目标
        :param module:
        :return:返回模块链整体抓取情况
        '''
        try:
            start_time = time.time()
            self.trace.trace(message=u"开始执行模块链")
            run_state = self.run_module(module)

            while run_state != EventType.COMPLETED:
                end_time = time.time()
                self.trace.trace(module, run_state, start_time, end_time)
                if run_state in [EventType.EXCEPTION_OCCURED, EventType.OUTPUT_NOT_SATISFIED, EventType.ASSERT_FAILED, EventType.WEB_CONTENT_FAILED]:
                    module.triggerEvent(run_state)
                    module_pre = module
                    module = self.getRedoModule(module, run_state)
                    if not module:
                        self.crawler.holder.logging.warning(u"模块[%s][%s]获取重试模块失败！将结束模块链执行！" % (module_pre.name, EventType.description(run_state)))
                        # 恢复模块动态变化属性为初始值
                        module_pre.recoverFromSnapshot()
                        return EventType.FAILED
                else:
                    module = module.getNextModule(self.crawler.value_dict)
                start_time = time.time()
                run_state = self.run_module(module)

            end_time = time.time()
            self.trace.trace(module, run_state, start_time, end_time)
            self.trace.trace(message=u"当前模块链执行结束")

            return run_state
        except Exception as e:
            self.error_handler(e)

    def getRedoModule(self, module, event_type):
        '''
        在模块执行状态异常时，获取重试模块，常见的异常状态：异常、未获取到期望输出、断言失败
        :param module: 当前模块
        :param event_type: 事件类型
        :return:
        '''
        if not module.events or event_type not in module.events:
            return None
        module_pre = module
        try:
            for event in module.events[event_type]:
                # 同一组中并不是每个事件都会被触发，例如Assert事件
                if not event.isTriggered:
                    continue
                if event.retry_times > 0:
                    event.retry_times -= 1
                    module = module.getRedoModule(event.redo_module)
                    self.recoverFirstModuleForRedo(module)
                    break
                elif event.retry_failed_strategy == RetryFailedStrategy.IGNORE:
                    return module.getNextModule(self.crawler.value_dict)
                elif event.retry_failed_strategy == RetryFailedStrategy.EXIT:
                    return None
                else:
                    return None
        except Exception as e:
            self.error_handler(e)
        finally:
            # 重置事件触发状态
            module_pre.untriggerEvent()
        self.crawler.holder.logging.info(u"模块[%s][%s]开始第 %s 次重试！" % (module_pre.name, EventType.description(event_type), module_pre.redo_times))
        return module

    def run_module(self, module):
        '''
        执行具体爬虫模块
        :param config_module:
        :return:
        '''
        try:
            if not module:
                return EventType.COMPLETED

            self.holder.logging.info(u"-------->开始执行模块 %s <--------", module.name)

            try:
                self.executeIputFunction(module)
                if module.function:
                    module.function(module)
                self.executeOutputFunction(module)
            except Exception as e:
                self.error_handler(e)
                return EventType.EXCEPTION_OCCURED

            try:
                self.valuesMonitor(module)
            except Exception as e:
                self.error_handler(e, u"监视中间结果出错！")

            try:
                self.executeExtraFunction(module)
            except Exception as e:
                self.error_handler(e, u"执行子类个性方法出错！")

            run_state = self.moduleResultValidation(module)
            # self.holder.logging.info("验证模块输出结果:%s", EventType.description(run_state))
            if run_state != EventType.NORMAL:
                return run_state

            if module.canIterate():
                return self.run_sub_modules_loop(module)
            return EventType.NORMAL
        except Exception as e:
            self.error_handler(e)
            return EventType.EXCEPTION_OCCURED

    def executeIputFunction(self, module):
        """
        执行输入参数提供的方法
        :param module: 当前执行模块
        :return:
        """
        # 可以没有output配置,例如聚合模块
        if not module.inputs:
            return EventType.NORMAL

        for input in module.inputs:
            if input.type == InputType.FUNCTION:
                value = util.run_function(input.value, self.crawler.value_dict, self.crawler.holder.logging)
                if not input.name and isinstance(value, dict):
                    self.crawler.value_dict.update(value)
                elif input.name:
                    self.crawler.value_dict[input.name] = value
        return EventType.NORMAL

    def executeOutputFunction(self, module):
        """
        执行输出参数提供的方法
        :param module:当前执行模块
        :return:
        """
        # 可以没有output配置,例如聚合模块
        if not module.outputs:
            return EventType.NORMAL

        for output in module.outputs:
            if output.type == OutputType.FUNCTION:
                value = util.run_function(output.function, self.crawler.value_dict, self.holder.logging)
                if not output.name and isinstance(value, dict):
                    self.crawler.value_dict.update(value)
                elif output.name:
                    self.crawler.value_dict[output.name] = value
        return EventType.NORMAL

    def executeExtraFunction(self, module):
        """
        执行爬虫子类个性方法
        :param module:
        :return:
        """
        if not module.extra_functions:
            return
        for func in module.extra_functions:
            util.run_function(func, self.crawler.value_dict, self.holder.logging)

    def valuesMonitor(self, module):
        """
        根据module配置监视相应的中间结果
        :param module:
        :return:
        """
        mm_dict = self.crawler.getMonitorMiddleValues(module)
        if not mm_dict:
            return
        self.holder.logging.info(u"监视中间结果输出")
        for key in mm_dict:
            if not key:
                self.holder.logging.error(u"未获取到 %s ！！！" % key)
            else:
                self.holder.logging.info(u"获取到%s=%s" % (key,mm_dict[key]))

    def moduleResultValidation(self, module):
        '''
        对模块执行结果依次进行验证：
        1.自定义断言是否成功, 断言判断须优先于抓取内容失败事件和预期结果的判断
        2.抓取过程中通过内容判断动态添加的内容抓取失败事件
        3.是否得到了预期的结果
        :param module:
        :return:
        '''
        if module.events:
            for event_key in module.events:
                if event_key == EventType.ASSERT_FAILED:
                    for event in module.events[event_key]:
                        assert_result = util.run_function(event.assert_function, self.crawler.value_dict, self.crawler.holder.logging)
                        if not assert_result:
                            module.triggerEvent(EventType.ASSERT_FAILED, event)
                            return EventType.ASSERT_FAILED
        if module.run_state != EventType.NORMAL:
            return module.run_state
        for output in module.outputs:
            if output.show_up == OutputParameterShowUpType.MUST:
                if not output.name:
                    continue
                if output.name not in self.crawler.value_dict:
                    return EventType.OUTPUT_NOT_SATISFIED
                value = self.crawler.value_dict[output.name]
                if not value:
                    return EventType.OUTPUT_NOT_SATISFIED
        return EventType.NORMAL
    
    def run_sub_modules_loop(self, module):
        '''
        循环执行子模块，可循环获取每个搜索列表中的公司信息
        :param module:包含子模块的父模块
        :return:
        '''
        iterator = module.iterator
        run_state = EventType.DO_NOTHING
        if iterator.seeds not in self.crawler.value_dict:
            return run_state
        company_list = self.crawler.value_dict[iterator.seeds]
        if not isinstance(company_list, list):
            return run_state
        for com in company_list:
            snap_id = uuid.uuid1()
            # 保留执行子模块之前的中间结果
            self.crawler.snapshot(snap_id)
            try:
                self.crawler.value_dict[iterator.param_name] = com
                if not module.modules:
                    return
                self.run_module_chain(module.modules[0])
            finally:
                # 恢复子模块之前的中间状态
                self.crawler.recoverFromSnapshot(snap_id)
        return EventType.NORMAL

    def snapFirstModuleForRedo(self, module):
        """
        执行第一个模块时，
        :param module:
        :return:
        """
        if not module or not self.crawler.module_manager.isFirstModule(module):
            return
        if not module.module_id:
            return
        self.crawler.snapshot(module.module_id)

    def recoverFirstModuleForRedo(self, module):
        """
        重试跳转到第一个模块时，恢复此前保存的中间状态
        :param module:
        :return:
        """
        if not module or not self.crawler.module_manager.isFirstModule(module):
            return
        if not module.module_id:
            return
        self.crawler.recoverFromSnapshot(module.module_id)

    def error_handler(self, e, error_message=None):
        '''
        统一处理异常
        :param e: 异常
        :param error_message:错误提示信息
        :return:
        '''
        self.error_prompt_message = error_message
        self.holder.logging.error(u"%s：%s" % (self.error_prompt_message, exceptutil.traceinfo(e)))

if __name__ == '__main__':
    pass
