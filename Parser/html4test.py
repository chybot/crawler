# -*- coding: utf-8 -*-
# Created by David on 2016/5/20.

html_shanghai = '''




<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>







<!-- 党组织主管/隶属单位字典 --><!-- 是否建立党组织字典 --><!-- 年报党建企业类型字典  --><!-- 团组织主管/隶属单位字典 --><!-- 是否建立团组织字典 --><!-- 其他部门公示信息行政许可查询类型 --><!-- 其他部门公示信息行政处罚查询类型 -->


<script type="text/javascript">
	// 常量类
	var constants = constants || {};

	// 是或否
	constants.yes = "1";
	constants.no = "0";

	// 即时公示已公示修改：业务类型
	constants.othAppSubType = {
		alt: "1",
		repeal: "2",
		revoke: "3",
		other: "4"
	};

	// 出资方式字典
	constants.dicInvtType = new Object();

		constants.dicInvtType["1"] = "货币";

		constants.dicInvtType["2"] = "实物";

		constants.dicInvtType["3"] = "知识产权";

		constants.dicInvtType["4"] = "债权";

		constants.dicInvtType["5"] = "高新技术成果";

		constants.dicInvtType["6"] = "土地使用权";

		constants.dicInvtType["7"] = "股权";

		constants.dicInvtType["8"] = "劳务";

		constants.dicInvtType["9"] = "其他";


	// 公示状态
	constants.dicNoticeState = new Object();

		constants.dicNoticeState["1"] = "已公示";

		constants.dicNoticeState["2"] = "未公示";

		constants.dicNoticeState["3"] = "未公示";


	// 登记信息状态字典
	constants.dicRegStatus = new Object();

		constants.dicRegStatus["1"] = "有效";

		constants.dicRegStatus["2"] = "无效";


	// 配置常量
	constants.config = {
		// 默认错误描述
		"err.default": "无法完成操作，请刷新页面后重试！"
	};

	// 全局变量类
	var global = global || {};

	// 当前服务器根路径
	global.base = "https://www.sgs.gov.cn/notice/";

	// 当前服务器时间
	global.current = '2016-05-19';

	// 当前年份
	global.year = '2016';

	// 当前令牌对象
	global.token = {
		name: "session.token",
		code: "91ef19bc-37ee-40ee-80e2-119d6d060c5a",
		data: {
			"session.token": "91ef19bc-37ee-40ee-80e2-119d6d060c5a"
		}
	};
</script>
<script type="text/javascript" src="https://www.sgs.gov.cn/notice/js/datepicker/WdatePicker.js?t=20151230-01"></script>
<base href="https://www.sgs.gov.cn/notice/" />
<link type="text/css" rel="stylesheet" href="js/ui/skin/smoothness/jquery-ui.css?t=20151230-01" />
<link type="text/css" rel="stylesheet" href="css/base.css?t=20151230-01" />

<script type="text/javascript" src="js/jquery.min.js?t=20151230-01"></script>
<script type="text/javascript" src="js/jquery.bgiframe.js?t=20151230-01"></script>
<script type="text/javascript" src="js/ui/jquery-ui.min.js?t=20151230-01"></script>
<script type="text/javascript" src="js/validate/jquery.validate.min.js?t=20151230-01"></script>
<script type="text/javascript" src="js/validate/validate.common.js?t=20151230-01"></script>
<script type="text/javascript" src="js/datepicker/WdateInit.js?t=20151230-01"></script>
<script type="text/javascript" src="js/loading/loading.js?t=20151230-01"></script>
<script type="text/javascript" src="js/loading/loading.bind.ajax.js?t=20151230-01"></script>
<script type="text/javascript" src="js/security/md5.min.js?t=20151230-01"></script>
<script type="text/javascript" src="js/math/BigDecimal-all-last.min.js?t=20151230-01"></script>
<script type="text/javascript" src="js/common.js?t=20151230-01"></script>
<script type="text/javascript" src="js/security/captcha.js?t=20151230-01"></script>
<script type="text/javascript" src="js/user/login.conf.sh.js?t=20151230-01"></script>
<script type="text/javascript" src="js/user/login.js?t=20151230-01"></script>
<script type="text/javascript" src="js/page/page.js?t=20151230-01" ></script>
<script type="text/javascript" src="js/search/search.js?t=20151230-01"></script>
<script type="text/javascript" src="js/json2.js?t=20151230-01"></script>

<!--[if lt IE 10]>
<script type="text/javascript" src="js/PIE.js?t=20151230-01"></script>
<script type="text/javascript" src="js/class.js?t=20151230-01"></script>
<![endif]-->
<!--[if lt IE 9]>
<script type="text/javascript" src="js/html5.js?t=20151230-01"></script>
<![endif]-->
<!--[if lt IE 7]>
<script type="text/javascript" src="js/DD_belatedPNG.js?t=20151230-01"></script>
<script type="text/javascript">
	DD_belatedPNG.fix("img");
</script>
<![endif]-->

<link type="text/css" rel="stylesheet" href="css/notice.css?t=20151230-01" />
<script type="text/javascript" src="js/page/page.notice.js?t=20151230-01" ></script>




<title>


		全国企业信用信息公示系统

</title>

    <style type="text/css">
    	.layout .header { background-image:url(images/layout/header-sh.png); }
    </style>

	<script type="text/javascript">
		// 自适应工作区域高度（通用页面）
		var autofitCommon = function() {
		};

		// 自适应工作区域高度（自适应事件调用）
		var autofit = autofitCommon;

		$(function() {
			// 初始化及页面大小变化时自适应工作区域高度
			$(window).resize(function() {
				autofit();
			}).load(function() {
				autofit();
				$(".layout").css("visibility", "visible");
			});
		});
	</script>
</head>
<body class="layout">
	<script type="text/javascript" src="js/loading/loading.bind.js?t=20151230-01"></script>

	<div class="header">




<ul class="nav">



			<li rel="nav-01" class="hide"><a href="http://gsxt.saic.gov.cn/">全国首页</a></li>
			<li rel="nav-02" class="hide"><a href="https://www.sgs.gov.cn/notice/home">地方局首页</a></li>


	<li rel="nav-06" class="hide"><a href="javascript:" onclick="help();return false;">使用帮助</a></li>
	<li rel="nav-03" class="hide"><a href="javascript:" onclick="login.clear();return false;">退出</a></li>
	<li rel="nav-04" class="hide"><a href="https://www.sgs.gov.cn/notice/report/home">返回</a></li>
	<li rel="nav-05" class="hide"><a href="https://www.sgs.gov.cn/notice/report/home?menu=offline">返回</a></li>


</ul>

<script type="text/javascript">
	$(function() {
		// 预设当前需显示的导航链接
		var navs = new Array();

			navs.push("01");

			navs.push("02");


		// 初始化导航栏显示
		toggleNav(navs);
	});

	// 切换导航栏链接显示
	function toggleNav(navs) {
		// 隐藏所有导航链接
		$(".nav li[rel]").hide();
		// 显示预设导航链接
		for(var i in navs) {
			$(".nav li[rel='nav-" + navs[i] + "']").show();
		}
	}

	// 下载使用帮助
	function help() {
		var iframe = $("iframe#download");

		if(iframe.size() == 0) {
			iframe = elem('<iframe src="javascript:" class="hide" id="download"></iframe>').appendTo("body");
		}

		iframe.attr("src", "https://www.sgs.gov.cn/notice/download/handbook?name=help.doc");
	}

	// 下载电子营业执照
	function licenceEx() {
		var iframe = $("iframe#download");

		if(iframe.size() == 0) {
			iframe = elem('<iframe src="javascript:" class="hide" id="download"></iframe>').appendTo("body");
		}

		iframe.attr("src", "https://www.sgs.gov.cn/notice/download/licenceEx?entId="+'');
	}
</script>
	</div>

	<div class="main">




























		<div class="notice">
			<ul class="title-bar clearfix invalid">
				<li>凯滢（上海）医疗器械有限公司</li>
				<li>注册号/统一社会信用代码：310000400735611          </li>


					<li>“该企业已列入经营异常名录”</li>

			</ul>

			<div class="cont clearfix">










<div class="cont-l">
	<ul>

			<li id="layout-01" onclick="tab('01', '01')">工商公示信息</li>

			<li id="layout-02" onclick="tab('02', '01')">企业公示信息</li>

			<li id="layout-03" onclick="tab('03', '01')">其他部门公示信息</li>

			<li id="layout-06" onclick="tab('06', '01')">司法协助公示信息</li>

	</ul>
</div>

<div class="cont-r">
	<div class="cont-r-t">
		<ul>

				<li id="layout-01_10" onclick="tab('01_10', '02')">
					<a href="javascript:" onclick="return false;">电子营业执照</a>
				</li>




					<li id="layout-01_01" onclick="tab('01_01', '02')">
						<a href="javascript:" onclick="return false;">登记信息</a>
					</li>




					<li id="layout-01_02" onclick="tab('01_02', '02')">
						<a href="javascript:" onclick="return false;">备案信息</a>
					</li>




					<li id="layout-01_04" onclick="tab('01_04', '02')">
						<a href="javascript:" onclick="return false;">动产抵押登记信息</a>
					</li>




					<li id="layout-01_03" onclick="tab('01_03', '02')">
						<a href="javascript:" onclick="return false;">股权出质登记信息</a>
					</li>




					<li id="layout-01_07" onclick="tab('01_07', '02')">
						<a href="javascript:" onclick="return false;">行政处罚信息</a>
					</li>




					<li id="layout-01_05" onclick="tab('01_05', '02')">
						<a href="javascript:" onclick="return false;">经营异常信息</a>
					</li>




					<li id="layout-01_06" onclick="tab('01_06', '02')">
						<a href="javascript:" onclick="return false;">严重违法信息</a>
					</li>




					<li id="layout-01_08" onclick="tab('01_08', '02')">
						<a href="javascript:" onclick="return false;">抽查检查信息</a>
					</li>




					<li id="layout-01_09" onclick="tab('01_09', '02')">
						<a href="javascript:" onclick="return false;">享受扶持信息</a>
					</li>

























		</ul>
	</div>
	<div class="cont-r-m">


			<span>&nbsp;</span>

	</div>
	<div class="cont-r-b">

			<div rel="layout-01_10" class="hide">






<!-- iframe -->
<iframe id="elIframe" src="" style="float:right; width:940px; _width:940px; min-height:969px; _height:882px;border:none;" ></iframe>

			</div>



				<div rel="layout-01_09" class="hide">










				</div>



				<div rel="layout-01_04" class="hide">







<table id="mortageTable" cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="5%"/><col width="20%"/><col width="15%"/><col width="20%"/><col width="20%"/><col width="10%"/><col width="10%"/>
	<tr>
		<th colspan="7">动产抵押登记信息</th>
	</tr>
	<tr>
		<th>序号</th>
		<th>登记编号</th>
		<th>登记日期</th>
		<th>登记机关</th>
		<th>被担保债权数额</th>
		<th>状态</th>
		<th>详情</th>
	</tr>

	<tr><th colspan="7" rel="10" class="page-container"></th></tr>
</table>


				</div>



				<div rel="layout-01_05" class="hide">















<table id="exceptTable" cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="5%"/><col width="25%"/><col width="15%"/><col width="25%"/><col width="15%"/><col width="15%"/>
	<tr>
		<th colspan="6">经营异常信息</th>
	</tr>
	<tr>
		<th>序号</th>
		<th>列入经营异常名录原因</th>
		<th>列入日期</th>
		<th>移出经营异常名录原因</th>
		<th>移出日期</th>
		<th>作出决定机关</th>
	</tr>

		<tr class="page-item">
			<td class="center">1</td>
			<td>未依照《企业信息公示暂行条例》第八条规定的期限公示2014年度年度报告的</td>
			<td class="center">2015年7月10日</td>
			<td></td>
			<td class="center"></td>
			<td>宝山区市场监督管理局</td>
		</tr>

	<tr><th colspan="6" rel="10" class="page-container"></th></tr>
</table>


				</div>



				<div rel="layout-01_03" class="hide">







<table id="pledgeTable" cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="5%" /><col width="10%" /><col width="10%" /><col width="12%" /><col width="10%" />
	<col width="10%" /><col width="12%" /><col width="15%" /><col width="8%" /><col width="8%" />
	<tr>
		<th colspan="10">股权出质登记信息</th>
	</tr>
    <tr>
		<th>序号</th>
		<th>登记编号</th>
		<th>出质人</th>
		<th>证照/证件号码</th>
		<th>出质股权数额</th>
		<th>质权人</th>
		<th>证照/证件号码</th>
		<th>股权出质设立登记日期</th>
		<th>状态</th>
		<th>变化情况</th>
	</tr>

	<tr><th colspan="10" rel="10" class="page-container"></th></tr>
</table>


				</div>



				<div rel="layout-01_06" class="hide">






<table id="blackTable" cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="5%"/><col width="25%"/><col width="15%"/><col width="25%"/><col width="15%"/><col width="15%"/>
	<tr>
		<th colspan="6">严重违法信息</th>
	</tr>
	<tr>
		<th>序号</th>
		<th>列入严重违法企业名单原因</th>
		<th>列入日期</th>
		<th>移出严重违法企业名单原因</th>
		<th>移出日期</th>
		<th>作出决定机关</th>
	</tr>

	<tr><th colspan="6" rel="10" class="page-container"></th></tr>
</table>


				</div>



				<div rel="layout-01_02" class="hide">






<table id="memberTable" cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="10%"/><col width="20%"/><col width="20%"/><col width="10%"/><col width="20%"/><col width="20%"/>
	<tr>
		<th colspan="6">主要人员信息</th>
	</tr>
	<tr>
		<th>序号</th>
		<th>姓名</th>
		<th>职务</th>
		<th>序号</th>
		<th>姓名</th>
		<th>职务</th>
	</tr>


			<tr class="page-item">

			<td class="center">1</td>
			<td>胡凯</td>
			<td>监事</td>




			<td class="center">2</td>
			<td>QIAN FUQING</td>
			<td>执行董事</td>


			</tr>


	<tr><th colspan="6" class="page-container"></th></tr>
</table>


				</div>



				<div rel="layout-01_01" class="hide">




























































<table cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="20%" /><col width="30%" /><col width="20%" /><col width="30%" />
	<tr>
		<th colspan="4">基本信息</th>
	</tr>
	<tr>
		<th class="right">注册号/<br>统一社会信用代码</th>
		<td>310000400735611          </td>
		<th class="right">名称</th>
		<td>凯滢（上海）医疗器械有限公司</td>
	</tr>
	<tr>
		<th class="right">类型</th>
		<td>有限责任公司(外国自然人独资)</td>
		<th class="right">法定代表人</th>
		<td>QIAN FUQING</td>
	</tr>






		<tr>
			<th class="right">注册资本</th>
			<td>55.000000万美元</td>
			<th class="right">成立日期</th>
			<td>2014年4月25日</td>
		</tr>



		<tr>
			<th class="right">住所</th>
			<td colspan="3">上海市宝山区宝林八村101号507室                                                                                                                                                                                                                                                                                                                                                              </td>
		</tr>




		<tr>
			<th class="right">经营期限自</th>
			<td>2014年4月25日</td>
			<th class="right">经营期限至</th>
			<td>2044年4月24日</td>
		</tr>


	<tr>
		<th class="right">经营范围</th>
		<td colspan="3">Ⅲ、Ⅱ类：口腔科材料，计算机软件及配件的批发、进出口业务，并提供相关配套服务；从事网络科技、计算机软硬件领域内的技术开发、技术咨询、技术转让、技术服务。【依法须经批准的项目，经相关部门批准后方可开展经营活动】</td>
	</tr>
	<tr>
		<th class="right">登记机关</th>
		<td>上海市工商局</td>
		<th class="right">核准日期</th>
		<td>2014年4月25日</td>
	</tr>

	<tr>



				<th class="right">登记状态</th>
				<td colspan="3">存续（在营、开业、在册）</td>



	</tr>



</table>

				</div>



				<div rel="layout-01_07" class="hide">







<table id="punishTable" cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="5%" /><col width="15%" /><col width="25%" /><col width="10%" />
	<col width="20%" /><col width="15%" /><col width="10%" />
	<tr>
		<th colspan="7">行政处罚信息</th>
	</tr>
	<tr>
		<th>序号</th>
		<th>行政处罚<br/>决定书文号</th>
		<th>违法行为类型</th>
		<th>行政处罚内容</th>
		<th>作出行政处罚<br/>决定机关名称</th>
		<th>作出行政处罚<br/>决定日期</th>
		<th>详情</th>
	</tr>

	<tr><th colspan="7" rel="20" class="page-container"></th></tr>
</table>


				</div>



				<div rel="layout-01_08" class="hide">






<table id="spotcheckTable" cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="5%"/><col width="25%"/><col width="15%"/><col width="15%"/><col width="40%"/>
	<tr>
		<th colspan="5">抽查检查信息</th>
	</tr>
	<tr>
		<th>序号</th>
		<th>检查实施机关</th>
		<th>类型</th>
		<th>日期</th>
		<th>结果</th>
	</tr>

	<tr><th colspan="6" rel="10" class="page-container"></th></tr>
</table>


				</div>



				<div rel="layout-01_02" class="hide">





<table id="branchTable" cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="10%"/><col width="20%"/><col width="40%"/><col width="30%"/>
	<tr><th colspan="4">分支机构信息</th></tr>
	<tr>
	  <th>序号</th>
	  <th>注册号/统一社会信用代码</th>
	  <th>名称</th>
	  <th>登记机关</th>
	</tr>

	<tr><th colspan="4" class="page-container"></th></tr>
</table>


				</div>



				<div rel="layout-01_01" class="hide">
















<table id="investorTable" cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="20%" /><col width="20%" /><col width="25%" /><col width="25%" /><col width="10%" />
	<tr>
		<th colspan="5">
			股东信息<br />
			<p>股东的出资信息截止2014年2月28日。2014年2月28日之后工商只公示股东姓名，其他出资信息由企业自行公示。</p>
		</th>
	</tr>
	<tr>
		<th>股东类型</th>
		<th>股东</th>
		<th>证照/证件类型</th>
		<th>证照/证件号码</th>
		<th>详情</th>
	</tr>

		<tr class="page-item">
			<td>外籍自然人</td>
			<td>QIAN FUQING</td>
			<td>


					外国（地区）护照

			</td>
			<td>




			</td>
			<td>
				<!-- 判断是否显示出资详情 -->

			</td>
		</tr>

	<tr><th colspan="5" class="page-container"></th></tr>
</table>


				</div>



				<div rel="layout-01_01" class="hide">






<table id="alterTable" cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="25%"/><col width="25%"/><col width="25%"/><col width="25%"/>
	<tr>
		<th colspan="4">变更信息</th>
	</tr>
	<tr>
		<th>变更事项</th>
		<th>变更前内容</th>
		<th>变更后内容</th>
		<th>变更日期</th>
	</tr>

	<tr><th colspan="4" class="page-container"></th></tr>
</table>


				</div>



				<div rel="layout-01_02" class="hide">










<table cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="20%"/><col width="20%"/><col width="20%"/><col width="20%"/><col width="20%"/>
	<tr><th colspan="5">清算信息</th></tr>





</table>


				</div>



				<div rel="layout-01_01" class="hide">






<table id="alterTable" cellspacing="0" cellpadding="0" class="info m-bottom m-top">
	<col width="25%"/><col width="25%"/><col width="25%"/><col width="25%"/>
	<tr>
		<th colspan="4">撤销信息</th>
	</tr>
	<tr>
		<th>撤销事项</th>
		<th>撤销前内容</th>
		<th>撤销后内容</th>
		<th>撤销日期</th>
	</tr>

	<tr><th colspan="4" class="page-container"></th></tr>
</table>


				</div>


























	</div>
</div>

<script type="text/javascript">
	$(function() {
		// 调整页面显示，使左侧标签页文字垂直居中，同时绑定hover事件
		$(".notice .cont-l li").each(function() {
			var li = $(this);
			var h = li.height();

			if(h <= parseInt(li.css("min-height"))) {
				var padding = (h - parseInt(li.css("line-height")) * $.trim(li.text()).length) / 2;
				li.css("padding-top", padding + "px");
				li.css("min-height", (h - padding) + "px");
			}
		}).hover(function() {
			$(this).addClass("hover");
		}, function() {
			$(this).removeClass("hover");
		});

		// 初始化左侧标签页选中状态
		$("#layout-01").addClass("current");

		// 控制是否加载司法协助公示信息股权变更标签页

			$("#layout-06_02, [rel='layout-06_02']").remove();
			$(".cont-r-t ul:empty").remove();


		// 控制是否加载工商公示-享受扶持信息签页

			$("#layout-01_09, [rel='layout-01_09']").remove();
			$(".cont-r-t ul:empty").remove();




				// 需要加载电子营业执照情况下工商公示信息默认显示登记信息
				$(".notice .cont-r-t li[id=layout-01_01]").click();



	});


		window.onload=function(){
			//判断是否加载电子营业执照标签
			ajaxCommon({
				url: $("base").attr("href") + "notice/is_elcense_needed",
				data: {
					uniScid:'',
					regNo:'310000400735611          '
				}
			}, function(result) {
				if(result == constants.no) {
					// 移出电子营业执照标签
					$("#layout-01_10, [rel='layout-01_10']").remove();
					$(".cont-r-t ul:empty").remove();
				}else{
					$("#elIframe").attr("src","http://218.242.124.22:8081/businessCheck/viewLicence_gs.do?attribute13=&attribute17=310000400735611");
				}
			});
		};


	// 点击标签页触发事件
	function tab(id, type) {
		// 当前选中的标签页对象
		var cur = $("#layout-" + id);

		// 如果标签页已经高亮选中，则直接返回
		if(cur.hasClass("current")) {
			return false;
		}

		if(type == "01") {
			// 跳转至相应公示信息标签页
			window.location = "https://www.sgs.gov.cn/notice/notice/view?uuid=nfc_corvFBzllR7Iop0WBeAkEqZHAcBK&tab=" + id;
		} else if(type == "02") {
			// 高亮选中标签页，并显示相应公示信息
			cur.addClass("current").siblings().removeClass("current");
			$("[rel='layout-" + id + "']").show().siblings("[rel!='layout-" + id + "']").hide();
		}
	}

</script>


			</div>
		</div>



<script type="text/javascript">
	$(function() {
		// 模拟分页效果
		$(".page-container").each(function() {
			var c = $(this);
			var i = c.parents("table").find(".page-item");
			var s = c.attr("rel") || 5; // 默认每页5条数据
			paging.simulate.init({
				container: c,
				items: i,
				size: s
			});
		});

		// 初始化td（收起多余的字）
		// td中内容需要收起的有格式要求 <td row="2" col="36" class="words">
		// row为显示的行数，col为显示的列数
		$(".words").each(function(){
			var words = $(this).html();
			var rowLen = $(this).attr("row");
			var colLen = $(this).attr("col");
			cutWords(rowLen,colLen,words,$(this));
		});
	});

	// 截取多余的汉字，并添加“更多”超链接
	function cutWords(rowLen, colLen, words, $td) {
		// td中字数
		var wordsLen = strlen(words);
		// 如果字数少于要求，则不作任何操作
		if(wordsLen <= rowLen*colLen) {
			return false;
		}
		// 截取后的内容
		var shortWords = cutstr(words, rowLen * colLen - 6);
		// 清除td中内容
		$td.html("");
		// 创建截取后字符的span，并添加到td中
		$(document.createElement("span")).attr("id", "shortWords").html(shortWords + " ").appendTo($td);
		// 创建“更多”超链接，并添加到td中
		$(document.createElement("a")).attr("href","javascript:;").attr("id","moreWordId").click(function() {
			moreWords(this);
			return false;
		}).html("更多").appendTo($td);
		// 创建所有字符span，并添加到td中
		$(document.createElement("span")).attr("id", "allWords").addClass("hide").html(words + " ").appendTo($td);
		// 创建“收起更多”超链接，并添加到td中
		$(document.createElement("a")).attr("href", "javascript:;").attr("id", "hideWordId").click(function() {
			hideWords(this);
			return false;
		}).html("收起更多").appendTo($td).hide();
	}

	// 更多
	function moreWords(a) {
		// 找到容器td
		$td = $(a).parents(".words");
		$td.find("#moreWordId, #shortWords").hide();
		$td.find("#allWords, #hideWordId").show();
	}

	// 收起更多
	function hideWords(a) {
		// 找到容器td
		$td = $(a).parents(".words");
		$td.find("#shortWords, #moreWordId").show();
		$td.find("#allWords, #hideWordId").hide();
	}
</script>
	</div>

	<div class="footer">
		<p>
			<span>版权所有：上海市工商行政管理局</span>
			<span>地址：上海市徐汇区肇嘉浜路301号</span>
			<span>邮政编码：200032</span>
		</p>
		<p>






					<span>业务咨询电话：021-12315</span>
					<span>技术支持电话：021-64220000-1002</span>





		</p>
	</div>


</body>
</html>
'''

html_jilin = '''






<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>

<meta name="_csrf_parameter" content="_csrf" /><meta name="_csrf_header" content="X-CSRF-TOKEN" /><meta name="_csrf" content="bbfda8d4-1155-4d67-89d7-5d9596da3d29" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>全国企业信用信息公示系统</title>
<link href="/aiccips/skin/css/public3.css" type="text/css" rel="stylesheet" />
<script type="text/javascript" src="/aiccips/skin/js/jquery-1.9.1.min.js"></script>
<script type="text/javascript" src="/aiccips/skin/js/gs/utils.js" ></script>
<script type="text/javascript" src="/aiccips/skin/js/gs/gsgs.js" ></script>
<script type="text/javascript" src="/aiccips/skin/js/gs/gsjyyc.js" ></script>
<script type="text/javascript">
	var encrpripid = '68243441c78560c0fa98f2b553e4648df3c56a105d5f339b6e4b31a5cbf317be61aecf898a7fcaa27626ee40c8c2864e';
	var webroot ='/aiccips/';
	var enttype='3200';
	function r1() {
		$("#jibenxinxi").css("display", "block");
		$("#beian").css("display", "none");
		$("#dongchandiya").css("display", "none");
		$("#jingyingyichangminglu").css("display", "none");
		$("#yanzhongweifaqiye").css("display", "none");
		$("#xingzhengchufa").css("display", "none");
		$("#chouchaxinxi").css("display", "none");
	}
	function r2() {
		$("#jibenxinxi").css("display", "none");
		$("#beian").css("display", "block");
		$("#dongchandiya").css("display", "none");
		$("#jingyingyichangminglu").css("display", "none");
		$("#yanzhongweifaqiye").css("display", "none");
		$("#xingzhengchufa").css("display", "none");
		$("#chouchaxinxi").css("display", "none");
		getCzxx();
	}

	function r4() {
		$("#jibenxinxi").css("display", "none");
		$("#beian").css("display", "none");
		$("#dongchandiya").css("display", "block");
		$("#jingyingyichangminglu").css("display", "none");
		$("#yanzhongweifaqiye").css("display", "none");
		$("#xingzhengchufa").css("display", "none");
		$("#chouchaxinxi").css("display", "none");
		getDcdy();
	}
	function r5() {
		$("#jibenxinxi").css("display", "none");
		$("#beian").css("display", "none");
		$("#dongchandiya").css("display", "none");
		$("#jingyingyichangminglu").css("display", "block");
		$("#yanzhongweifaqiye").css("display", "none");
		$("#xingzhengchufa").css("display", "none");
		$("#chouchaxinxi").css("display", "none");
		getJyyc();
	}
	function r6() {
		$("#jibenxinxi").css("display", "none");
		$("#beian").css("display", "none");
		$("#dongchandiya").css("display", "none");
		$("#jingyingyichangminglu").css("display", "none");
		$("#yanzhongweifaqiye").css("display", "block");
		$("#xingzhengchufa").css("display", "none");
		$("#chouchaxinxi").css("display", "none");
		getYzwfqy();
	}
	function r7() {
		$("#jibenxinxi").css("display", "none");
		$("#beian").css("display", "none");
		$("#dongchandiya").css("display", "none");
		$("#jingyingyichangminglu").css("display", "none");
		$("#yanzhongweifaqiye").css("display", "none");
		$("#xingzhengchufa").css("display", "block");
		$("#chouchaxinxi").css("display", "none");
		getXzcf();
		}
   function r8() {
		$("#jibenxinxi").css("display", "none");
		$("#beian").css("display", "none");
		$("#dongchandiya").css("display", "none");
		$("#jingyingyichangminglu").css("display", "none");
		$("#yanzhongweifaqiye").css("display", "none");
		$("#xingzhengchufa").css("display", "none");
		$("#chouchaxinxi").css("display", "block");
		 getCcjc();
	}


	function togo(str) {
		if (str == '1') {
			window.location = '../../gsgsdetail/3200/68243441c78560c0fa98f2b553e4648df3c56a105d5f339b6e4b31a5cbf317be61aecf898a7fcaa27626ee40c8c2864e';
		} else if (str == '2') {
			window.location = '../../qygsdetail/3200/68243441c78560c0fa98f2b553e4648df3c56a105d5f339b6e4b31a5cbf317be61aecf898a7fcaa27626ee40c8c2864e';
		} else if (str == '3') {
			window.location = '../../qtgsdetail/3200/68243441c78560c0fa98f2b553e4648df3c56a105d5f339b6e4b31a5cbf317be61aecf898a7fcaa27626ee40c8c2864e';
		} else if (str == '4') {
			window.location = '../../sfgsdetail/3200/68243441c78560c0fa98f2b553e4648df3c56a105d5f339b6e4b31a5cbf317be61aecf898a7fcaa27626ee40c8c2864e';
		}
	}
</script>
<script type="text/javascript">
var bgsxliststr ='[]';
var bgsxlist=null;
$(document)
.ready(
		function() {
			var isindex=true;
			var fromjyyc=true;
			var fromccjc=true;
			if(!isindex){
				if(fromjyyc){
					r5();
					changeStyle('tabs',$("#5"));
				}
				else if(fromccjc){
						r8();
						changeStyle('tabs',$("#8"));
				}
			}
			//变更事项
			if(''!=bgsxliststr){
				bgsxliststr=bgsxliststr;
				bgsxlist =eval('('+bgsxliststr.replace(/\r/ig, "").replace(/\n/ig, "")+')');
			    setbgsxpagenumbers(bgsxlist.length);//出资信息分页
			    bgsxpage(1);
			}
		});
//变更信息分页
function setbgsxpagenumbers(size){
	if(size==0) return;
	var  count=Math.ceil(size/5);
	$("#bgsxpages").append("<span><a href='javascript:bgsxpage(1);'>&lt;&lt;</a></span>&nbsp;&nbsp;");
	for (var i = 0; i <count; i++) {
		$("#bgsxpages").append("<a href='javascript:bgsxpage("+(i+1)+");'>"+(i+1)+"</a>&nbsp;&nbsp;");
	};
	$("#bgsxpages").append("</span><span><a href='javascript:bgsxpage("+count+");'>&gt;&gt;</a></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
}
//变更事项分页
function bgsxpage(page){
	$("#bgsxtable").children().remove();
	var recordHtml="";
	var altbe="";
	var altaf="";
	for (var i= 5*(page-1); i < 5*page; i++) {
		if(i<bgsxlist.length){
			var bgsx=bgsxlist[i];
			altbe=(null!=bgsx.altbe&&undefined !=bgsx.altbe?bgsx.altbe:"");
			altaf=(null!=bgsx.altaf&&undefined !=bgsx.altaf?bgsx.altaf:"");
			recordHtml="<tr><td>"+ bgsx.altitem + "</td><td>";
			if(altbe.length>40){
				recordHtml+='<span id="beless'+i+'" style="display:block">';
				recordHtml+=altbe.substring(0,40);
				recordHtml+='<a href="###" onclick="v1h2(\'bemore'+i+'\',\'beless'+i+'\')">更多</a></span>';
				recordHtml+='<span id="bemore'+i+'" style="display:none">';
				recordHtml+=altbe;
				recordHtml+='<a href="###" onclick="v1h2(\'beless'+i+'\',\'bemore'+i+'\')">收起更多</a></span>';
			}else{
				recordHtml+=altbe;
			}
			recordHtml+="</td><td>";
			 if(altaf.length>40){
				 recordHtml+='<span id="afless'+i+'" style="display:block">';
				 recordHtml+=altaf.substring(0,40);
				 recordHtml+='<a href="###" onclick="v1h2(\'afmore'+i+'\',\'afless'+i+'\')">更多</a></span>';
				 recordHtml+='<span id="afmore'+i+'" style="display:none">';
				 recordHtml+=altaf;
				 recordHtml+='<a href="###" onclick="v1h2(\'afless'+i+'\',\'afmore'+i+'\')">收起更多</a></span>';
			 }else{
				 recordHtml+=altaf;
			 }
			 recordHtml+="</td><td>"+ (JsonSetTime(bgsx.altdate))+"</td></tr>";

			$("#bgsxtable").append(recordHtml);
		}
	}
}
</script>
<script type="text/javascript" defer="defer">
	function changeStyle(divId, ele) {
		var liAry = document.getElementById(divId).getElementsByTagName("li");
		var liLen = liAry.length;
		var liID = ele.id;
		for (var i = 0; i < liLen; i++) {
			if (liAry[i].id == liID) {
				liAry[i].className = "current";

			} else {
				liAry[i].className = "";
			}
			;
		}
		;
	}

	function ShowSpan(obj, n) {
		var span = obj.parentNode.getElementsByTagName("tabs");
		for (var i = 0; i < span.length; i++) {
			span[i].className = "current";
		}
		span[n].className = "";
		var li = obj.parentNode.getElementsByTagName("li");
		li[n].className = "current";
		for (var i = 0; i < li.length; i++) {
			if (i != n) {
				li[i].className = "";
			}
			li[i].onmouseout = function() {
				this.className = "current";
			};
		}
		;
	}
	function v1h2(first,second){
		$("#"+first+"").css("display", "block");
		$("#"+second+"").css("display", "none");
	}
</script>
</head>
<body>
	<div id="header">







		 <div class="top">
				<div class="top-a">
					<a href="http://gsxt.saic.gov.cn/">全国首页</a>
					&nbsp;&nbsp;
					 <a href="/aiccips/">地方局首页</a>
				</div>
			</div>



	</div>
	<br />
	<br />
	<br />
	<br />
	<div id="details" class="clear">
		<h2 id="mct"    >黑龙江省中和国际经济贸易公司珲春公司&nbsp;&nbsp;
			&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp; 注册号/统一社会信用代码：24478567-6
			</h2>
		<br />
		<div id="leftTabs">
			<ul>
				<li class="current" style="margin-bottom: 2px;"><p>
						工<br />商<br />公<br />示<br />信<br />息
					</p></li>
				<li onclick="togo('2')" style="margin-bottom: 2px;"><p>
						企<br />业<br />公<br />示<br />信<br />息
					</p></li>
				<li onclick="togo('3')" style="margin-bottom: 2px;"><p>
						其<br />他<br />部<br />门<br />公<br />示<br />信<br />息
					</p></li>

			</ul>
  </div>
  <div id="detailsCon" style="height:auto !important;height:1030px;min-height:1030px ;"  >
			<div class="dConBox">
				<div class="tabs" id="tabs">
        <ul>
					<li id="1" class="current" onclick="r1(),changeStyle('tabs',this)">登记信息</li>
					<li id="2" onclick="r2(),changeStyle('tabs',this)">备案信息</li>
					<li id="4" onclick="r4(),changeStyle('tabs',this)">动产抵押登记信息</li>
					<li id="7" onclick="r7(),changeStyle('tabs',this)">行政处罚信息</li>
					<li id="5" onclick="r5(),changeStyle('tabs',this)">经营异常信息</li>
					<li id="6" onclick="r6(),changeStyle('tabs',this)">严重违法信息</li>
					<li id="8" onclick="r8(),changeStyle('tabs',this)">抽查检查信息</li>
        </ul>
				</div>

				<div id="jibenxinxi">
					<br />
					<table cellspacing="0" cellpadding="0" class="detailsList">
						<tr>
							<th colspan="4" style="text-align: center;">基本信息</th>
						</tr>
						<tr>
							<th width="20%">注册号/统一社会信用代码</th>
							<td width="30%">24478567-6</td>
							<th>名称</th>
							<td width="30%">黑龙江省中和国际经济贸易公司珲春公司</td>
						</tr>
						<tr>
							<th>类型</th>
							<td>集体所有制</td>
							<th width="20%">法定代表人</th>
							<td>金立家</td>
						</tr>
						<tr>
							<th>住所</th>
							<td colspan="3">珲春市靖和街新兴委28号</td>
						</tr>
		<tr>
			<th width="20%">注册资本</th>
							<td>

							 	30万元人民币
								</td>
							<th width="20%">成立日期</th>
							<td>1993年04月10日</td>
						</tr>
						<tr>
							<th>经营期限自</th>
							<td>1993年04月10日</td>
							<th>经营期限至</th>
							<td></td>
						</tr>
						<tr>
							<th>经营范围<br /></th>
							<td colspan="3">批发零售：开展易货贸易、销售易货挽回的商品***（依法须经批准的项目，经相关部门批准后方可开展经营活动）</td>
						</tr>
						<tr>
							<th>登记机关</th>
							<td>珲春市工商行政管理局</td>
							<th>核准日期</th>
							<td>1998年10月08日</td>
						</tr>
						<tr>
							<th>登记状态</th>
							<td>吊销企业</td>


							  		    <th>吊销日期</th>
										<td>1998年10月08日</td>



						</tr>
					</table>
					<br />
					<table cellpadding="0" cellspacing="0" class="detailsList">
					<tr  style="width: 95%;"><th colspan="4" style="text-align:center;">变更信息</th></tr>
					<tr  style="width: 95%;">
					<th width="15%" style="text-align:center;"> 变更事项</th>
					<th width="25%" style="text-align:center;"> 变更前内容</th>
					<th width="25%" style="text-align:center;"> 变更后内容</th>
					<th width="10%" style="text-align:center;"> 变更日期</th>
					</tr>
				   <tbody id="bgsxtable"></tbody>
					</table>
					<table cellpadding="0" cellspacing="0" class="detailsList">
						<tr>
							<th id="bgsxpages" colspan="5" style="text-align: rigth;">
						</th>
						</tr>
					</table>

				</div>
				<div id="beian" style="align: center; display: none">
					<br />
			  <table style="width:100%;" id="t30" cellpadding="0" cellspacing="0" class="detailsList">
					<tr  style="width: 939px;">
            <th colspan="5" style="text-align:center;">主管部门（出资人）信息</th>
          </tr>
          <tr>
            <th style="width:10%;text-align:center">序号</th>
            <th style="width:20%;text-align:center">出资人类型</th>
            <th style="width:20%;text-align:center">出资人</th>
            <th style="width:20%;text-align:center">证照/证件类型</th>
            <th style="width:20%;text-align:center">证照/证件号码</th>
					</tr>
						<tbody id="gsgsCzxxList"></tbody>
					</table>
					<br />
				</div>
				<div id="dongchandiya" style="display: none">
					<br />
					<table cellpadding="0" cellspacing="0" class="detailsList">
							<tr  style="width: 95%;"><th colspan="7" style="text-align:center;">动产抵押信息</th></tr>
					<tr  style="width: 95%;">
						<th width="5%" style="text-align:center;">序号</th>
						<th width="25%" style="text-align:center;">登记编号</th>
						<th width="15%" style="text-align:center;">登记日期</th>
						<th width="20%" style="text-align:center;">登记机关</th>
						<th width="15%" style="text-align:center;">被担保债权数额</th>
						<th width="10%" style="text-align:center;">状态</th>
						<th width="10%" style="text-align:center;">详情</th>
					</tr>
						<tbody id='gsgsDcdylist'></tbody>
					</table>
					<br />
				</div>

				<div id="jingyingyichangminglu" style="display: none">
				<br/>
				<table  cellpadding="0" cellspacing="0" class="detailsList">
							<tr  style="width: 95%;"><th colspan="9" style="text-align:center;">经营异常信息</th></tr>
					<tr  style="width: 95%;">
						<th width="5%"style="text-align:center;">序号</th>
						<th width="25%"style="text-align:center;">列入经营异常名录原因</th>
						<th width="10%"style="text-align:center;">列入日期</th>
						<th width="27%"style="text-align:center;">移出经营异常名录原因</th>
						<th width="10%"style="text-align:center;">移出日期</th>
						<th width="10%"style="text-align:center;">作出决定机关</th>
					</tr>
						<tbody id='gsgsjyyclist'></tbody>
					</table>
					<br />
				</div>

				<div id="yanzhongweifaqiye" style="display: none">
				<br/>
				<table  cellpadding="0" cellspacing="0" class="detailsList">
							<tr ><th colspan="6" style="text-align:center;">严重违法信息</th></tr>
					<tr  style="width: 95%;">
						<th width="5%"style="text-align:center;">序号</th>
						<th width="25%"style="text-align:center;">列入严重违法企业名单原因</th>
						<th width="13%"style="text-align:center;">列入日期</th>
						<th width="20%"style="text-align:center;">移出严重违法企业名单原因</th>
						<th width="13%"style="text-align:center;">移出日期</th>
						<th width="24%"style="text-align:center;">作出决定机关</th>
					</tr>
						<tbody id='gsgsyzwflsit'></tbody>
					</table>
					<br />
				</div>


	    	<div id="xingzhengchufa"  style="display:none">
 				<br/>
				<table  cellpadding="0" cellspacing="0" class="detailsList">
							<tr  style="width: 95%;"><th colspan="7" style="text-align:center;">行政处罚信息</th></tr>
					<tr  style="width: 95%;">
						<th width="5%"style="text-align:center;">序号</th>
						<th width="10%"style="text-align:center;">行政处罚<br/>决定书文号</th>
						<th width="20%"style="text-align:center;">违法行为类型</th>
						<th width="10%"style="text-align:center;">行政处罚内容</th>
						<th width="10%"style="text-align:center;">作出行政处罚<br/>决定机关名称</th>
						<th width="10%"style="text-align:center;">作出行政处罚<br/>决定日期</th>
						<th width="10%"style="text-align:center;">详情</th>
					</tr>
					<tbody id='gsgsxzcflist'></tbody>
				</table><br/>
			</div>

				<div id="chouchaxinxi" style="display: none">
				<br/>
				<table  cellpadding="0" cellspacing="0" class="detailsList">
							<tr  style="width: 95%;"><th colspan="5" style="text-align:center;">抽查检查信息</th></tr>
					<tr  style="width: 95%;">
						<th width="5%"style="text-align:center;">序号</th>
						<th width="35%"style="text-align:center;">检查实施机关</th>
						<th width="10%"style="text-align:center;">类型</th>
						<th width="15%"style="text-align:center;">日期</th>
						<th width="35%"style="text-align:center;">结果</th>
					</tr>
						<tbody id='gsgsccjclist'></tbody>
					</table>
					<br />
				</div>

			</div>
		</div>
		<div class="banqun">



    版权所有：吉林省工商行政管理局&nbsp;&nbsp;&nbsp;&nbsp;地址：长春市南湖大路599号&nbsp;&nbsp;&nbsp;&nbsp;邮政编码：130000<br />
             <img  width="30" height="25"  alt="业务（技术）咨询电话" src="/aiccips/skin/images/phone.png" align="middle" >
<span style="height: 30px;vertical-align:middle;">：
 <a  href="/aiccips/phone.html" style="color: white;" target="_blank"><u>业务（技术）咨询电话</u></a> </span>
<script type="text/javascript">var cnzz_protocol = (("https:" == document.location.protocol) ? " https://" : " http://");document.write(unescape("%3Cspan id='cnzz_stat_icon_1000300906'%3E%3C/span%3E%3Cscript src='" + cnzz_protocol + "s5.cnzz.com/z_stat.php%3Fid%3D1000300906%26show%3Dpic1' type='text/javascript'%3E%3C/script%3E"));</script>


		</div>
	</div>
</body>
</html>

'''

html_jiangxi_top = '''







<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>全国企业信用信息公示系统</title>
	<script type="text/javascript" src="http://gsxt.jxaic.gov.cn:80/ECPS//include/js/jquery-1.9.0.min.js"></script>
	<link rel="stylesheet" type="text/css" href="http://gsxt.jxaic.gov.cn:80/ECPS//include/css/public3.css"/>
	<link rel="stylesheet" type="text/css" href="http://gsxt.jxaic.gov.cn:80/ECPS//include/css/style.css"/>

	<script type="text/javascript">
		var src = "";
		function r1(qyid,zch,qylx,num){
			src = "/ECPS/ccjcgs/gsgs_viewDjxx.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&num="+num+"&showgdxx=true";
			$('#gsgsIframe').attr("src",src);
		}
		function r2(qyid,zch,qylx){
			src = "/ECPS/ccjcgs/gsgs_viewBaxx.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&showgdxx=true";
			$('#gsgsIframe').attr("src",src);
		}
		function r3(qyid,zch,qylx){
			src = "/ECPS/ccjcgs/gsgs_viewGqczdjxx.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&showgdxx=true";
			$('#gsgsIframe').attr("src",src);
		}
		function r4(qyid,zch,qylx,num){
			src = "/ECPS/ccjcgs/gsgs_viewDcdydjxx.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&num="+num+"&showgdxx=true";
			$('#gsgsIframe').attr("src",src);
		}
		function r5(qyid,zch,qylx){
			src = "/ECPS/ccjcgs/gsgs_viewJyycxx.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&showgdxx=true";
			$('#gsgsIframe').attr("src",src);
		}
		function r6(qyid,zch,qylx){
			src = "/ECPS/ccjcgs/gsgs_viewYzwfxx.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&showgdxx=true";
			$('#gsgsIframe').attr("src",src);
		}
		function r7(qyid,zch,qylx,num){
			src = "/ECPS/ccjcgs/gsgs_viewXzcfxx.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&num="+num+"&showgdxx=true";
			$('#gsgsIframe').attr("src",src);
		}
		function r8(qyid,zch,qylx){
			src = "/ECPS/ccjcgs/gsgs_viewCcjcxx.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&showgdxx=true";
			$('#gsgsIframe').attr("src",src);
		}
		function r10(qyid,zch,qylx,num){
			src = "/ECPS/ccjcgs/qygs_ViewQynb.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&num="+num + "&showgdxx=true";
			$('#qygsIframe').attr("src",src);
		}
		function r11(qyid){
			src = "/ECPS/qygs/gdjcz_viewGdjcz.pt?qyid="+qyid+"&qygsxx=1" + "&showgdxx=true";
			$('#qygsIframe').attr("src",src);
		}
		function r12(qyid){
			src = "/ECPS/qygs/gqbg_viewGqbg.pt?qyid="+qyid+"&qygsxx=1" + "&showgdxx=true";
			$('#qygsIframe').attr("src",src);
		}
		function r13(qyid,zch,qylx,num,qymc){
			src = "/ECPS/qygs/xzxk_viewXzxk.pt?qyid="+qyid+"&qygsxx=1"+"&zch="+zch+"&qylx="+qylx+"&num="+num+"&qymc="+qymc + "&showgdxx=true";
			$('#qygsIframe').attr("src",src);
		}
		function r14(qyid,zch,qylx,num,qymc){
			src = "/ECPS/qygs/zscqczdj_viewZscqczdj.pt?qyid="+qyid+"&qygsxx=1"+"&zch="+zch+"&qylx="+qylx+"&num="+num+"&qymc="+qymc + "&showgdxx=true";
			$('#qygsIframe').attr("src",src);
		}
		function r15(qyid){
			src = "/ECPS/qygs/xzcf_viewXzcf.pt?qyid="+qyid+"&qygsxx=1" + "&showgdxx=true";
			$('#qygsIframe').attr("src",src);
		}

		function r16(qyid,zch,qylx,num){
			src = "/ECPS/ccjcgs/qygs_ViewQtbmxzxk.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&num="+num;
			$('#qtbmIfram').attr("src",src);
		}
		function r17(qyid,zch,qylx,num){
			src = "/ECPS/ccjcgs/qygs_ViewQtbmxzcf.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&num="+num;
			$('#qtbmIfram').attr("src",src);
		}
		function r18(qyid,zch,qylx,num){
			src = "/ECPS/sfxz/gqdj_gqdjList.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&num="+num;
			$('#sfxzIfram').attr("src",src);
		}
		function r19(qyid,zch,qylx,num){
			src = "/ECPS/sfxz/gdbg_gdbgList.pt?qyid="+qyid+"&zch="+zch+"&qylx="+qylx+"&num="+num;
			$('#sfxzIfram').attr("src",src);
		}
		function togo(str){
			if(str=='1'){
		 			//window.location='查询企业信息-工商公示.html';
		 			document.getElementById("detailsCon1").style.display = "block";
		 			document.getElementById("detailsCon2").style.display = "none";
		 			document.getElementById("detailsCon3").style.display = "none";
		 			document.getElementById("detailsCon4").style.display = "none";
		 			document.getElementById("togo1").className = "current";
		 			document.getElementById("togo2").className = "";
		 			document.getElementById("togo3").className = "";
		 			document.getElementById("togo4").className = "";
			}else if(str=='2'){
		 			//window.location='查询企业信息-企业公示.html';
		 			document.getElementById("detailsCon1").style.display = "none";
		 			document.getElementById("detailsCon2").style.display = "block";
		 			document.getElementById("detailsCon3").style.display = "none";
		 			document.getElementById("detailsCon4").style.display = "none";
		 			document.getElementById("togo1").className = "";
		 			document.getElementById("togo2").className = "current";
		 			document.getElementById("togo3").className = "";
		 			document.getElementById("togo4").className = "";

		 			r10('3606002012081600243944','9136060006346630XD','1229','0');
			}else if(str=='3'){
		 			//window.location='查询企业信息-其他部门公示信息.html';
		 			document.getElementById("detailsCon1").style.display = "none";
		 			document.getElementById("detailsCon2").style.display = "none";
		 			document.getElementById("detailsCon3").style.display = "block";
		 			document.getElementById("detailsCon4").style.display = "none";
		 			document.getElementById("togo1").className = "";
		 			document.getElementById("togo2").className = "";
		 			document.getElementById("togo3").className = "current";
		 			document.getElementById("togo4").className = "";
		 			r16('3606002012081600243944','9136060006346630XD','1229','0');
			}else if(str=='4'){
		      //window.location='查询企业信息-司法协助公示.html';
		     		document.getElementById("detailsCon1").style.display = "none";
		 			document.getElementById("detailsCon2").style.display = "none";
		 			document.getElementById("detailsCon3").style.display = "none";
		 			document.getElementById("detailsCon4").style.display = "block";
		 			document.getElementById("togo1").className = "";
		 			document.getElementById("togo2").className = "";
		 			document.getElementById("togo3").className = "";
		 			document.getElementById("togo4").className = "current";
		 			r18('3606002012081600243944','9136060006346630XD','1229','0');
		  }
		}
	</script>
	<script type="text/javascript" defer="defer">
		 function changeStyle(divId,ele){
            var liAry=document.getElementById(divId).getElementsByTagName("li");
            var liLen=liAry.length;
            var liID=ele.id;
            for(var i=0;i<liLen;i++)
            {
                if(liAry[i].id==liID)
                {
                    liAry[i].className="current";

                }
                else
                {
                   liAry[i].className="";
                }
            }
        }
		$(function() {
			//默认选中所给tab页
			document.getElementById('1').className = "current";
			eval("r1('3606002012081600243944','9136060006346630XD','1229')");
		});
	</script>
</head>
<body>
<div id="header">
	 <!--首页TOP  -->
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<div class="top">
	<div class="top-a">
		<a href="http://gsxt.saic.gov.cn/" target="_blank">全国首页</a>
	</div>
</div>


<div id="details" class="clear">
	<div style="height: 40px; line-height: 40px; font-size: 16px;" id="gsh3">
  	 &nbsp;鹰潭市信江海融小额贷款股份有限公司&nbsp;&nbsp;注册号/统一社会信用代码：9136060006346630XD&nbsp;&nbsp;
	</div>
    <br/>
	<div id="leftTabs" >
	    <ul>
	      <li onclick="togo('1')" id="togo1" class="current" style="margin-bottom:2px;height:240px;"><p>工<br />商<br />公<br />示<br />信<br />息</p></li>
	      <li onclick="togo('2')" id="togo2" style="margin-bottom:2px;height:240px;"><p>企<br />业<br />公<br />示<br />信<br />息</p></li>
	      <li onclick="togo('3')" id="togo3" style="margin-bottom:2px;height:240px;"><p>其<br />他<br />部<br />门<br />公<br />示<br />信<br />息</p></li>
	      <li onclick="togo('4')" id="togo4" style="margin-bottom:2px;height:240px;"><p>司<br />法<br />协<br />助<br />公<br />示<br />信<br />息</p></li>
	    </ul>
	</div>
	<div id="detailsCon1" class="detailsConClass" style="display: block;">
	    <div class="dConBox"  style="height: 100%;">
	      <div class="tabs" id="tabs">
	        <ul>
				<li id="1" onclick="r1('3606002012081600243944','9136060006346630XD','1229','0' ),changeStyle('tabs',this)">登记信息</li>
				<li id="2" onclick="r2('3606002012081600243944','9136060006346630XD','1229'),changeStyle('tabs',this)">备案信息</li>
				<li id="4" onclick="r4('3606002012081600243944','9136060006346630XD','1229','0'),changeStyle('tabs',this)">动产抵押登记信息</li>
				<li id="3" onclick="r3('3606002012081600243944','9136060006346630XD','1229'),changeStyle('tabs',this)">股权出质登记信息</li>
				<li id="7" onclick="r7('3606002012081600243944','9136060006346630XD','1229','0' ),changeStyle('tabs',this)">行政处罚信息</li>
				<li id="5" onclick="r5('3606002012081600243944','9136060006346630XD','1229'),changeStyle('tabs',this)">经营异常信息</li>
				<li id="6" onclick="r6('3606002012081600243944','9136060006346630XD','1229'),changeStyle('tabs',this)">严重违法信息</li>
				<li id="8" onclick="r8('3606002012081600243944','9136060006346630XD','1229'),changeStyle('tabs',this)">抽查检查信息</li>
	        </ul>
	      </div>

	       <!-- 工商公示信息 -->
	      <div class="iframeHeightClass">
	      		<iframe id="gsgsIframe" src="" width="100%" height="100%;" scrolling="auto" frameborder="0"></iframe>
	      </div>
		</div>
    </div>
    <div id="detailsCon2" class="detailsConClass" style="display: none;">
	    <div class="dConBox" style="height: 100%;">
	      <div class="tabs" id="tabs2">
	        <ul>
		  		<li id="10" class="current"  onclick="r10('3606002012081600243944','9136060006346630XD','1229','0' ),changeStyle('tabs2',this)">企业年报</li>
				<li id="11"  onclick="r11('3606002012081600243944'),changeStyle('tabs2',this)">股东及出资信息</li>
				<li id="12"  onclick="r12('3606002012081600243944'),changeStyle('tabs2',this)">股权变更信息</li>
				<li id="13"  onclick="r13('3606002012081600243944','9136060006346630XD','1229','0','鹰潭市信江海融小额贷款股份有限公司'),changeStyle('tabs2',this)">行政许可信息</li>
				<li id="14"  onclick="r14('3606002012081600243944','9136060006346630XD','1229','0','鹰潭市信江海融小额贷款股份有限公司'),changeStyle('tabs2',this)">知识产权出质登记信息</li>
				<li id="15"  onclick="r15('3606002012081600243944'),changeStyle('tabs2',this)">行政处罚信息</li>

	        </ul>
	      </div>
		  <h2 id="qiyeTitle" style="text-align:center;">企业公示信息由该企业提供，企业对其公示信息的真实性、合法性负责</h2>

		 <!-- 企业公示信息 -->
	      <div class="iframeHeightClass">
	      		<iframe id="qygsIframe" src="" width="100%" height="100%" scrolling="no" frameborder="0"></iframe>
	      </div>
	    </div>
	</div>

	<div id="detailsCon3" class="detailsConClass" style="height:970px;display: none;">
	    <div class="dConBox">
	      <div class="tabs" id="tabs3">
	        <ul>
		  		<li id="16" class="current"  onclick="r16('3606002012081600243944','9136060006346630XD','1229','0'),changeStyle('tabs3',this)">行政许可信息</li>
				<li id="17"  onclick="r17('3606002012081600243944','9136060006346630XD','1229','0'),changeStyle('tabs3',this)">行政处罚信息</li>
	        </ul>
	      </div>

	      <!-- 其他部门公示信息 -->
	      <div class="iframeHeightClass">
	      		<iframe id="qtbmIfram" src="http://gsxt.jxaic.gov.cn:80/ECPS/common/common_showNull.pt" width="100%" height="100%" scrolling="no" frameborder="0"></iframe>
	      </div>
    	</div>
	</div>
	<div id="detailsCon4" class="detailsConClass" style="height:970px;display: none;">
    	<div class="dConBox">
			<div class="tabs" id="tabs4">
		        <ul>
		        <li id="18" class="current"  onclick="r18('3606002012081600243944','9136060006346630XD','1229','0'),changeStyle('tabs4',this)">股权冻结信息</li>
		        <li id="19"  onclick="r19('3606002012081600243944','9136060006346630XD','1229','0'),changeStyle('tabs4',this)">股东变更信息</li>
		        </ul>
	        </div>

	         <!-- 司法协助公示信息 -->
	      	<div class="iframeHeightClass">
	      		<iframe id="sfxzIfram" src="" width="100%" height="100%" scrolling="no" frameborder="0"></iframe>
		    </div>
		</div>

	</div>
	<!--首页底部  -->

<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style>
<!--
a{
	font-size: 14px;
}
-->
</style>
<div class="banqun" style="line-height: 23px;">
                  版权所有：江西省工商行政管理局&nbsp;&nbsp;&nbsp;&nbsp;地址：江西省南昌市省府大院东三路2号 &nbsp;&nbsp;&nbsp;&nbsp;邮政编码：330046<br />
                  企业咨询电话：<a href="/ECPS/home/home_downLoad.pt?path=zxdh.doc" style="color: #ffffff;">查看详情</a>；
                  个体农专咨询电话：<a href="/ECPS/home/home_downLoad.pt?path=gtzxdh.doc" style="color: #ffffff;">查看详情</a>&nbsp;&nbsp;&nbsp;
                  技术支持电话：<a href="/ECPS/home/home_downLoad.pt?path=jszc.doc" style="color: #ffffff;">查看详情</a> &nbsp;&nbsp;&nbsp;
                  建议使用谷歌、IE8及以上版本浏览器  <a href="http://rj.baidu.com/search/index/?kw=ie8" target="_blank" style="color: #ffffff;">点击下载</a>
</div>

</div>
</div>
</body>
</html>
'''