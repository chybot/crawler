# -*- coding: utf-8 -*-
# Created by David on 2016/4/20.

enterprise_html_base='''

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet" />
	<link href="/country_credit/bj/css/style.css" type="text/css" rel="stylesheet" />
	<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script><!-- 1.9版本jQuery js   1-->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/pubInfo.js"></script><!-- 北京首页pubInfo.js js   -->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/gs_tab.js"></script><!-- 工商公示 tab页签的变化 js   -->
	<script type="text/javascript">
	var rootPath = '';
 	var entId = 'DCBB0FD56D324C87AD672F5D35EA3437';
	var entName = '北京百度网讯科技有限公司';
	var entNo = '110108002734659';
	var type = '';
	var checkCodeServletName = "CheckCodeCaptcha";
	$(document).ready(function(){
	    if(!type){
		    gsCheckCurrentTab('djxxDiv',entId);
		}else{
		    gsCheckCurrentTab(type,entId);
		}
	});


//工商公示 页面显示tab也内容显示
function gsCheckCurrentTab(currentId,entId){
	var liAIdArr =['djxxDiv','bgxxDiv','dcdyDiv','gqczdjDiv','xzcfDiv','jyycDiv','yzwfDiv','ccycDiv'];
	for(var i=0;i<liAIdArr.length;i++){
		if(currentId==liAIdArr[i]){
			$("#"+currentId).css('display','block');
			if(currentId=='djxxDiv'){//登记信息
				var entName = encodeURIComponent(jQuery.trim(entName));
				$("#tzrFrame").attr("src",rootPath+"/gjjbj/gjjQueryCreditAction!tzrFrame.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entId))+"&entName="+entName+"&clear=true&timeStamp="+new Date().getTime());//给该url一个时间戳~~这样就必须每次从服务器读取数据
				$("#bgxxFrame").attr("src",rootPath+"/gjjbj/gjjQueryCreditAction!biangengFrame.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='bgxxDiv'){//变更信息
				$("#zyryFrame").attr("src",rootPath+"/gjjbj/gjjQueryCreditAction!zyryFrame.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
				$("#fzjgFrame").attr("src",rootPath+"/gjjbj/gjjQueryCreditAction!fzjgFrame.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entName))+"&clear=true&timeStamp="+new Date().getTime());
				ajaxChange(entId);
			}else if(currentId=='dcdyDiv'){//动产抵押
				$("#dcdyFrame").attr("src",rootPath+"/gjjbjTab/gjjTabQueryCreditAction!dcdyFrame.dhtml?entId="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='gqczdjDiv'){//股权出质登记信息
				 $("#gqczdjFrame").attr("src",rootPath+"/gdczdj/gdczdjAction!gdczdjFrame.dhtml?entId="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='xzcfDiv'){//行政处罚
				$("#xzcfFrame").attr("src",rootPath+"/gsgs/gsxzcfAction!list.dhtml?entId="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='jyycDiv'){//经营异常
				$("#jyycFrame").attr("src",rootPath+"/gsgs/gsxzcfAction!list_jyycxx.dhtml?entId="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='yzwfDiv'){//严重违法
				$("#yzwfFrame").attr("src",rootPath+"/gsgs/gsxzcfAction!list_yzwfxx.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='ccycDiv'){//抽查检查
				$("#ccycFrame").attr("src",rootPath+"/gsgs/gsxzcfAction!list_ccjcxx.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}
		}else{
			$("#"+liAIdArr[i]).css('display','none');
		}
	}
}
	</script>
</head>
<body>
<div id="header">
	<div class="top">
		<div class="top-a">
			<a href="#"  onclick="toCountryIndex();">全国首页</a>
			<a href="#" onclick="toIndex();">地方局首页</a>
		 </div> <!-- 新的tab头 -->
	</div>
</div>
<div id="details" class="clear">

		<h2> 北京百度网讯科技有限公司 &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;

  		  	注册号：110108002734659
  		   &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;
  	 </h2>




   <br/>
   <div id="leftTabs">
	    <ul>
	      <li class="current" style="margin-bottom:2px;"><p>工<br />商<br />公<br />示<br />信<br />息</p></li>

				 <li onclick="togo('2','82B9F118C3E2ACEA775235B21EACCAE9')" style="margin-bottom:2px;"><p>企<br />业<br />公<br />示<br />信<br />息</p></li>

	     <li onclick="togo('3','82B9F118C3E2ACEA775235B21EACCAE9')"><p style="padding-top:15px;">其<br />他<br />部<br />门<br />公<br />示<br />信<br />息</p></li>
	    </ul>
   </div>

   	<div id="detailsCon" style="min-height:800px;height:auto;">
   		<div class="dConBox" >
   			  <div class="tabs" id="tabs">
			       <ul>
							<li id="0" class="current" onclick="gsCheckCurrentTab('djxxDiv','DCBB0FD56D324C87AD672F5D35EA3437'),changeStyle('tabs',this)">登记信息</li>
							<li id="1" onclick="gsCheckCurrentTab('bgxxDiv','DCBB0FD56D324C87AD672F5D35EA3437'),changeStyle('tabs',this)">备案信息</li>
					       	<li id="2" onclick="gsCheckCurrentTab('dcdyDiv','DCBB0FD56D324C87AD672F5D35EA3437'),changeStyle('tabs',this)">动产抵押登记信息</li>
							<li id="3" onclick="gsCheckCurrentTab('gqczdjDiv','DCBB0FD56D324C87AD672F5D35EA3437'),changeStyle('tabs',this)">股权出质登记信息</li>
							<li id="4" onclick="gsCheckCurrentTab('xzcfDiv','DCBB0FD56D324C87AD672F5D35EA3437'),changeStyle('tabs',this)">行政处罚信息</li>
							<li id="5"  onclick="gsCheckCurrentTab('jyycDiv','DCBB0FD56D324C87AD672F5D35EA3437'),changeStyle('tabs',this)">经营异常信息</li>
							<li id="6"  onclick="gsCheckCurrentTab('yzwfDiv','DCBB0FD56D324C87AD672F5D35EA3437'),changeStyle('tabs',this)">严重违法信息</li>
							<li id="7"  onclick="gsCheckCurrentTab('ccycDiv','DCBB0FD56D324C87AD672F5D35EA3437'),changeStyle('tabs',this)">抽查检查信息</li>
						 </ul>
		      </div>
		      <br/>
		      <!-- 登记信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
		       <div id="djxxDiv">
			      <div id="jbxx">


						<!-- 内资公司法人 -->





<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet" />
</head>
<body>
	 <table cellspacing="0" cellpadding="0" class="detailsList" >
	      	<tr>
	      		<th colspan="4" style="text-align:center;">基本信息 </th>
	      	</tr>

	      	<tr>

		        <th width="20%">注册号</th>
	         	<td width="30%">110108002734659</td>

	          <th>名称</th>
	          <td width="30%">北京百度网讯科技有限公司</td>
	        </tr>

	        <tr>
		        <th>类型</th>
		        <td>有限责任公司(自然人投资或控股)</td>
		        <th width="20%">法定代表人</th>
		        <td>梁志祥</td>
	        </tr>

	         <tr>
		        <th>注册资本</th>
		        <td>

			      	   10000 万元

			      </td>
		        <th width="20%">成立日期</th>
	             <td>2001年06月05日</td>
	        </tr>
	        <tr>
	           <th>住所</th>
	           <td colspan="3">北京市海淀区上地十街10号百度大厦2层</td>
	        </tr>
	         <tr>
	        	<th>营业期限自</th>
	            <td>2001年06月05日</td>
	         	 <th>营业期限至</th>
	           <td>2021年06月04日</td>
	        </tr>

	         <tr>
	          <th>经营范围</th>
	         <td colspan="3">因特信息服务业务（除出版、教育、医疗保健以外的内容）；第一类增值电信业务中的在线数据处理与交易处理业务、国内因特网虚拟专用网业务、因特网数据中心业务；第二类增值电信业务中的因特网接入服务业务、呼叫中心业务、信息服务业务（不含固定网电话信息服务和互联网信息服务）（增值电信业务经营许可证有效期至2015年10月20日）；利用互联网经营音乐娱乐产品，游戏产品运营，网络游戏虚拟货币发行，美术品，演出剧（节）目，动漫（画）产品，从事互联网文化产品展览、比赛活动（网络文化经营许可证有效期至2016年11月21日）；设计、开发、销售计算机软件；技术服务、技术培训、技术推广；经济信息咨询；利用www.baidu.com、www.hao123.com(www.hao222.net、www.hao222.com)、网站发布广告；设计、制作、代理、发布广告；货物进出口、技术进出口、代理进出口；医疗软件技术开发；委托生产电子产品、玩具、照相器材；销售家用电器、机械设备、五金交电、电子产品、文化用品、照相器材、计算机、软件及辅助设备、化妆品、卫生用品、体育用品、纺织品、服装、鞋帽、日用品、家具、首饰、避孕器具、工艺品、钟表、眼镜、玩具、汽车及摩托车配件、仪器仪表、塑料制品、花、草及观赏植物、建筑材料、通讯设备；预防保健咨询。（依法须经批准的项目，经相关部门批准后依批准内容开展经营活动。）</td>
	        </tr>
	         <tr>
	          <th width="20%">登记机关</th>
	          <td>北京市工商行政管理局</td>
	          <th>核准日期</th>
	          <td>2015年01月12日</td>
	        </tr>
	         <tr>
	        	<th>登记状态</th>
		        <td>在营（开业）企业</td>

        	          <th width="20%"></th>
      	              <td></td>

	        </tr>
	   </table>
</body>
</html>

			      </div><br/>
			      <div id="tzr">
			      		<iframe id="tzrFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div><br/>
			      <div id="bgxx">
			      		<iframe id="bgxxFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
		      </div>
		       <!-- 备案信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
		      <div id="bgxxDiv"  style="display:none">
			      <div id="zyry">
			      		<iframe id="zyryFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div><br/>
				  <div id="fzjg">
				  		<iframe id="fzjgFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
				  </div><br/>
				  <div id="qsxx">
				  </div>
			  </div>
			   <!-- 动产抵押登记信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
			   <div id="dcdyDiv"  style="display:none">
			      <div id="dcdy">
			      		<iframe id="dcdyFrame" scrolling="no"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>
			   <!-- 股权出质登记信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
			   <div id="gqczdjDiv"  style="display:none">
			      <div id="gqczdj">
			      		<iframe id="gqczdjFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>
			   <!-- 行政处罚信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
			  <div id="xzcfDiv"  style="display:none">
			      <div id="xzcf">
			      		<iframe id="xzcfFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>
			   <!-- 经营异常信息 ~~~~~~~~~~~begin~~~~~~~~~ -->
			  <div id="jyycDiv"  style="display:none">
			      <div id="jyyc">
			      		<iframe id="jyycFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>
			   <!-- 严重违法信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
			  <div id="yzwfDiv"  style="display:none">
			      <div id="yzwf">
			      		<iframe id="yzwfFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>
			   <!-- 抽查检查信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
			  <div id="ccycDiv"  style="display:none">
			      <div id="ccyc">
			      		<iframe id="ccycFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>

  		 </div>
  	</div>
<div class="banqun" style="padding-bottom:20px;margin-top:10px;">
              版权所有：北京市工商行政管理局&nbsp;&nbsp;&nbsp;&nbsp;地址：北京市海淀区苏州街36号&nbsp;&nbsp;&nbsp;&nbsp;邮政编码：100080<br />
              <!-- 业务咨询电话：010-82691213，010-82691523&nbsp;&nbsp;&nbsp;&nbsp;技术支持电话：010-82691768（公示），010-82691101（年报） -->
</div>
  </div>
</body>
</html> '''

enterprise_html_partner='''
<html xmlns="http://www.w3.org/1999/xhtml"><head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet">
	<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script><!-- 1.9版本jQuery js   -->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/pubInfo.js"></script><!-- 北京首页pubInfo.js js   -->
	<script type="text/javascript">
	var rootPath = '';
 	var entId = 'DCBB0FD56D324C87AD672F5D35EA3437';
	var entName = '';
	var entNo = '';

	function viewInfo(entId){
		var inv = encodeURIComponent(jQuery.trim(entId));
		var entName = encodeURIComponent(jQuery.trim(entName));
		var url = rootPath + "/gjjbj/gjjQueryCreditAction!touzirenInfo.dhtml?chr_id="+inv+"&entName="+entName+"&timeStamp="+new Date().getTime()+"&fqr=";//给该url一个时间戳~~这样就必须每次从服务器读取数据;
		window.open(url);
	}
	</script>
	<style>
	html { overflow:hidden; }
	</style>
<style class="firebugResetStyles" type="text/css" charset="utf-8">/* See license.txt for terms of usage */
/** reset styling **/
.firebugResetStyles {
    z-index: 2147483646 !important;
    top: 0 !important;
    left: 0 !important;
    display: block !important;
    border: 0 none !important;
    margin: 0 !important;
    padding: 0 !important;
    outline: 0 !important;
    min-width: 0 !important;
    max-width: none !important;
    min-height: 0 !important;
    max-height: none !important;
    position: fixed !important;
    transform: rotate(0deg) !important;
    transform-origin: 50% 50% !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    background: transparent none !important;
    pointer-events: none !important;
    white-space: normal !important;
}
style.firebugResetStyles {
    display: none !important;
}

.firebugBlockBackgroundColor {
    background-color: transparent !important;
}

.firebugResetStyles:before, .firebugResetStyles:after {
    content: "" !important;
}
/**actual styling to be modified by firebug theme**/
.firebugCanvas {
    display: none !important;
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
.firebugLayoutBox {
    width: auto !important;
    position: static !important;
}

.firebugLayoutBoxOffset {
    opacity: 0.8 !important;
    position: fixed !important;
}

.firebugLayoutLine {
    opacity: 0.4 !important;
    background-color: #000000 !important;
}

.firebugLayoutLineLeft, .firebugLayoutLineRight {
    width: 1px !important;
    height: 100% !important;
}

.firebugLayoutLineTop, .firebugLayoutLineBottom {
    width: 100% !important;
    height: 1px !important;
}

.firebugLayoutLineTop {
    margin-top: -1px !important;
    border-top: 1px solid #999999 !important;
}

.firebugLayoutLineRight {
    border-right: 1px solid #999999 !important;
}

.firebugLayoutLineBottom {
    border-bottom: 1px solid #999999 !important;
}

.firebugLayoutLineLeft {
    margin-left: -1px !important;
    border-left: 1px solid #999999 !important;
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
.firebugLayoutBoxParent {
    border-top: 0 none !important;
    border-right: 1px dashed #E00 !important;
    border-bottom: 1px dashed #E00 !important;
    border-left: 0 none !important;
    position: fixed !important;
    width: auto !important;
}

.firebugRuler{
    position: absolute !important;
}

.firebugRulerH {
    top: -15px !important;
    left: 0 !important;
    width: 100% !important;
    height: 14px !important;
    background: url("data:image/png,%89PNG%0D%0A%1A%0A%00%00%00%0DIHDR%00%00%13%88%00%00%00%0E%08%02%00%00%00L%25a%0A%00%00%00%04gAMA%00%00%D6%D8%D4OX2%00%00%00%19tEXtSoftware%00Adobe%20ImageReadyq%C9e%3C%00%00%04%F8IDATx%DA%EC%DD%D1n%E2%3A%00E%D1%80%F8%FF%EF%E2%AF2%95%D0D4%0E%C1%14%B0%8Fa-%E9%3E%CC%9C%87n%B9%81%A6W0%1C%A6i%9A%E7y%0As8%1CT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AATE9%FE%FCw%3E%9F%AF%2B%2F%BA%97%FDT%1D~K(%5C%9D%D5%EA%1B%5C%86%B5%A9%BDU%B5y%80%ED%AB*%03%FAV9%AB%E1%CEj%E7%82%EF%FB%18%BC%AEJ8%AB%FA'%D2%BEU9%D7U%ECc0%E1%A2r%5DynwVi%CFW%7F%BB%17%7Dy%EACU%CD%0E%F0%FA%3BX%FEbV%FEM%9B%2B%AD%BE%AA%E5%95v%AB%AA%E3E5%DCu%15rV9%07%B5%7F%B5w%FCm%BA%BE%AA%FBY%3D%14%F0%EE%C7%60%0EU%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5JU%88%D3%F5%1F%AE%DF%3B%1B%F2%3E%DAUCNa%F92%D02%AC%7Dm%F9%3A%D4%F2%8B6%AE*%BF%5C%C2Ym~9g5%D0Y%95%17%7C%C8c%B0%7C%18%26%9CU%CD%13i%F7%AA%90%B3Z%7D%95%B4%C7%60%E6E%B5%BC%05%B4%FBY%95U%9E%DB%FD%1C%FC%E0%9F%83%7F%BE%17%7DkjMU%E3%03%AC%7CWj%DF%83%9An%BCG%AE%F1%95%96yQ%0Dq%5Dy%00%3Et%B5'%FC6%5DS%95pV%95%01%81%FF'%07%00%00%00%00%00%00%00%00%00%F8x%C7%F0%BE%9COp%5D%C9%7C%AD%E7%E6%EBV%FB%1E%E0(%07%E5%AC%C6%3A%ABi%9C%8F%C6%0E9%AB%C0'%D2%8E%9F%F99%D0E%B5%99%14%F5%0D%CD%7F%24%C6%DEH%B8%E9rV%DFs%DB%D0%F7%00k%FE%1D%84%84%83J%B8%E3%BA%FB%EF%20%84%1C%D7%AD%B0%8E%D7U%C8Y%05%1E%D4t%EF%AD%95Q%BF8w%BF%E9%0A%BF%EB%03%00%00%00%00%00%00%00%00%00%B8vJ%8E%BB%F5%B1u%8Cx%80%E1o%5E%CA9%AB%CB%CB%8E%03%DF%1D%B7T%25%9C%D5(%EFJM8%AB%CC'%D2%B2*%A4s%E7c6%FB%3E%FA%A2%1E%80~%0E%3E%DA%10x%5D%95Uig%15u%15%ED%7C%14%B6%87%A1%3B%FCo8%A8%D8o%D3%ADO%01%EDx%83%1A~%1B%9FpP%A3%DC%C6'%9C%95gK%00%00%00%00%00%00%00%00%00%20%D9%C9%11%D0%C0%40%AF%3F%EE%EE%92%94%D6%16X%B5%BCMH%15%2F%BF%D4%A7%C87%F1%8E%F2%81%AE%AAvzr%DA2%ABV%17%7C%E63%83%E7I%DC%C6%0Bs%1B%EF6%1E%00%00%00%00%00%00%00%00%00%80cr%9CW%FF%7F%C6%01%0E%F1%CE%A5%84%B3%CA%BC%E0%CB%AA%84%CE%F9%BF)%EC%13%08WU%AE%AB%B1%AE%2BO%EC%8E%CBYe%FE%8CN%ABr%5Dy%60~%CFA%0D%F4%AE%D4%BE%C75%CA%EDVB%EA(%B7%F1%09g%E5%D9%12%00%00%00%00%00%00%00%00%00H%F6%EB%13S%E7y%5E%5E%FB%98%F0%22%D1%B2'%A7%F0%92%B1%BC%24z3%AC%7Dm%60%D5%92%B4%7CEUO%5E%F0%AA*%3BU%B9%AE%3E%A0j%94%07%A0%C7%A0%AB%FD%B5%3F%A0%F7%03T%3Dy%D7%F7%D6%D4%C0%AAU%D2%E6%DFt%3F%A8%CC%AA%F2%86%B9%D7%F5%1F%18%E6%01%F8%CC%D5%9E%F0%F3z%88%AA%90%EF%20%00%00%00%00%00%00%00%00%00%C0%A6%D3%EA%CFi%AFb%2C%7BB%0A%2B%C3%1A%D7%06V%D5%07%A8r%5D%3D%D9%A6%CAu%F5%25%CF%A2%99%97zNX%60%95%AB%5DUZ%D5%FBR%03%AB%1C%D4k%9F%3F%BB%5C%FF%81a%AE%AB'%7F%F3%EA%FE%F3z%94%AA%D8%DF%5B%01%00%00%00%00%00%00%00%00%00%8E%FB%F3%F2%B1%1B%8DWU%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*UiU%C7%BBe%E7%F3%B9%CB%AAJ%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5J%95*U%AAT%A9R%A5*%AAj%FD%C6%D4%5Eo%90%B5Z%ADV%AB%D5j%B5Z%ADV%AB%D5j%B5Z%ADV%AB%D5j%B5Z%ADV%AB%D5j%B5Z%ADV%AB%D5j%B5Z%ADV%AB%D5j%B5Z%ADV%AB%D5j%B5%86%AF%1B%9F%98%DA%EBm%BBV%AB%D5j%B5Z%ADV%AB%D5j%B5Z%ADV%AB%D5j%B5Z%ADV%AB%D5j%B5Z%ADV%AB%D5j%B5Z%ADV%AB%D5j%B5Z%ADV%AB%D5j%B5Z%AD%D6%E4%F58%01%00%00%00%00%00%00%00%00%00%00%00%00%00%40%85%7F%02%0C%008%C2%D0H%16j%8FX%00%00%00%00IEND%AEB%60%82") repeat-x !important;
    border-top: 1px solid #BBBBBB !important;
    border-right: 1px dashed #BBBBBB !important;
    border-bottom: 1px solid #000000 !important;
}

.firebugRulerV {
    top: 0 !important;
    left: -15px !important;
    width: 14px !important;
    height: 100% !important;
    background: url("data:image/png,%89PNG%0D%0A%1A%0A%00%00%00%0DIHDR%00%00%00%0E%00%00%13%88%08%02%00%00%00%0E%F5%CB%10%00%00%00%04gAMA%00%00%D6%D8%D4OX2%00%00%00%19tEXtSoftware%00Adobe%20ImageReadyq%C9e%3C%00%00%06~IDATx%DA%EC%DD%D1v%A20%14%40Qt%F1%FF%FF%E4%97%D9%07%3BT%19%92%DC%40(%90%EEy%9A5%CB%B6%E8%F6%9Ac%A4%CC0%84%FF%DC%9E%CF%E7%E3%F1%88%DE4%F8%5D%C7%9F%2F%BA%DD%5E%7FI%7D%F18%DDn%BA%C5%FB%DF%97%BFk%F2%10%FF%FD%B4%F2M%A7%FB%FD%FD%B3%22%07p%8F%3F%AE%E3%F4S%8A%8F%40%EEq%9D%BE8D%F0%0EY%A1Uq%B7%EA%1F%81%88V%E8X%3F%B4%CEy%B7h%D1%A2E%EBohU%FC%D9%AF2fO%8BBeD%BE%F7X%0C%97%A4%D6b7%2Ck%A5%12%E3%9B%60v%B7r%C7%1AI%8C%BD%2B%23r%00c0%B2v%9B%AD%CA%26%0C%1Ek%05A%FD%93%D0%2B%A1u%8B%16-%95q%5Ce%DCSO%8E%E4M%23%8B%F7%C2%FE%40%BB%BD%8C%FC%8A%B5V%EBu%40%F9%3B%A72%FA%AE%8C%D4%01%CC%B5%DA%13%9CB%AB%E2I%18%24%B0n%A9%0CZ*Ce%9C%A22%8E%D8NJ%1E%EB%FF%8F%AE%CAP%19*%C3%BAEKe%AC%D1%AAX%8C*%DEH%8F%C5W%A1e%AD%D4%B7%5C%5B%19%C5%DB%0D%EF%9F%19%1D%7B%5E%86%BD%0C%95%A12%AC%5B*%83%96%CAP%19%F62T%86%CAP%19*%83%96%CA%B8Xe%BC%FE)T%19%A1%17xg%7F%DA%CBP%19*%C3%BA%A52T%86%CAP%19%F62T%86%CA%B0n%A9%0CZ%1DV%C6%3D%F3%FCH%DE%B4%B8~%7F%5CZc%F1%D6%1F%AF%84%F9%0F6%E6%EBVt9%0E~%BEr%AF%23%B0%97%A12T%86%CAP%19%B4T%86%CA%B8Re%D8%CBP%19*%C3%BA%A52huX%19%AE%CA%E5%BC%0C%7B%19*CeX%B7h%A9%0C%95%E1%BC%0C%7B%19*CeX%B7T%06%AD%CB%5E%95%2B%BF.%8F%C5%97%D5%E4%7B%EE%82%D6%FB%CF-%9C%FD%B9%CF%3By%7B%19%F62T%86%CA%B0n%D1R%19*%A3%D3%CA%B0%97%A12T%86uKe%D0%EA%B02*%3F1%99%5DB%2B%A4%B5%F8%3A%7C%BA%2B%8Co%7D%5C%EDe%A8%0C%95a%DDR%19%B4T%C66%82fA%B2%ED%DA%9FC%FC%17GZ%06%C9%E1%B3%E5%2C%1A%9FoiB%EB%96%CA%A0%D5qe4%7B%7D%FD%85%F7%5B%ED_%E0s%07%F0k%951%ECr%0D%B5C%D7-g%D1%A8%0C%EB%96%CA%A0%A52T%C6)*%C3%5E%86%CAP%19%D6-%95A%EB*%95q%F8%BB%E3%F9%AB%F6%E21%ACZ%B7%22%B7%9B%3F%02%85%CB%A2%5B%B7%BA%5E%B7%9C%97%E1%BC%0C%EB%16-%95%A12z%AC%0C%BFc%A22T%86uKe%D0%EA%B02V%DD%AD%8A%2B%8CWhe%5E%AF%CF%F5%3B%26%CE%CBh%5C%19%CE%CB%B0%F3%A4%095%A1%CAP%19*Ce%A8%0C%3BO*Ce%A8%0C%95%A12%3A%AD%8C%0A%82%7B%F0v%1F%2FD%A9%5B%9F%EE%EA%26%AF%03%CA%DF9%7B%19*Ce%A8%0C%95%A12T%86%CA%B8Ze%D8%CBP%19*Ce%A8%0C%95%D1ae%EC%F7%89I%E1%B4%D7M%D7P%8BjU%5C%BB%3E%F2%20%D8%CBP%19*Ce%A8%0C%95%A12T%C6%D5*%C3%5E%86%CAP%19*Ce%B4O%07%7B%F0W%7Bw%1C%7C%1A%8C%B3%3B%D1%EE%AA%5C%D6-%EBV%83%80%5E%D0%CA%10%5CU%2BD%E07YU%86%CAP%19*%E3%9A%95%91%D9%A0%C8%AD%5B%EDv%9E%82%FFKOee%E4%8FUe%A8%0C%95%A12T%C6%1F%A9%8C%C8%3D%5B%A5%15%FD%14%22r%E7B%9F%17l%F8%BF%ED%EAf%2B%7F%CF%ECe%D8%CBP%19*Ce%A8%0C%95%E1%93~%7B%19%F62T%86%CAP%19*Ce%A8%0C%E7%13%DA%CBP%19*Ce%A8%0CZf%8B%16-Z%B4h%D1R%19f%8B%16-Z%B4h%D1R%19%B4%CC%16-Z%B4h%D1R%19%B4%CC%16-Z%B4h%D1%A2%A52%CC%16-Z%B4h%D1%A2%A52h%99-Z%B4h%D1%A2%A52h%99-Z%B4h%D1%A2EKe%98-Z%B4h%D1%A2EKe%D02%5B%B4h%D1%A2EKe%D02%5B%B4h%D1%A2E%8B%96%CA0%5B%B4h%D1%A2E%8B%96%CA%A0e%B6h%D1%A2E%8B%96%CA%A0e%B6h%D1%A2E%8B%16-%95a%B6h%D1%A2E%8B%16-%95A%CBl%D1%A2E%8B%16-%95A%CBl%D1%A2E%8B%16-Z*%C3l%D1%A2E%8B%16-Z*%83%96%D9%A2E%8B%16-Z*%83%96%D9%A2E%8B%16-Z%B4T%86%D9%A2E%8B%16-Z%B4T%06-%B3E%8B%16-Z%B4T%06-%B3E%8B%16-Z%B4h%A9%0C%B3E%8B%16-Z%B4h%A9%0CZf%8B%16-Z%B4h%A9%0CZf%8B%16-Z%B4h%D1R%19f%8B%16-Z%B4h%D1R%19%B4%CC%16-Z%B4h%D1R%19%B4%CC%16-Z%B4h%D1%A2%A52%CC%16-Z%B4h%D1%A2%A52h%99-Z%B4h%D1%A2%A52h%99-Z%B4h%D1%A2EKe%98-Z%B4h%D1%A2EKe%D02%5B%B4h%D1%A2EKe%D02%5B%B4h%D1%A2E%8B%96%CA0%5B%B4h%D1%A2E%8B%96%CA%A0e%B6h%D1%A2E%8B%96%CA%A0e%B6h%D1%A2E%8B%16-%95a%B6h%D1%A2E%8B%16-%95A%CBl%D1%A2E%8B%16-%95A%CBl%D1%A2E%8B%16-Z*%C3l%D1%A2E%8B%16-Z*%83%96%D9%A2E%8B%16-Z*%83%96%D9%A2E%8B%16-Z%B4T%86%D9%A2E%8B%16-Z%B4T%06-%B3E%8B%16-Z%B4T%06-%B3E%8B%16-Z%B4h%A9%0C%B3E%8B%16-Z%B4h%A9%0CZf%8B%16-Z%B4h%A9%0CZf%8B%16-Z%B4h%D1R%19f%8B%16-Z%B4h%D1R%19%B4%CC%16-Z%B4h%D1R%19%B4%CC%16-Z%B4h%D1%A2%A52%CC%16-Z%B4h%D1%A2%A52h%99-Z%B4h%D1%A2%A52h%99-Z%B4h%D1%A2EKe%98-Z%B4h%D1%A2EKe%D02%5B%B4h%D1%A2EKe%D02%5B%B4h%D1%A2E%8B%96%CA0%5B%B4h%D1%A2E%8B%96%CA%A0e%B6h%D1%A2E%8B%96%CA%A0e%B6h%D1%A2E%8B%16-%95a%B6h%D1%A2E%8B%16-%95A%CBl%D1%A2E%8B%16-%95A%CBl%D1%A2E%8B%16-Z*%C3l%D1%A2E%8B%16-Z*%83%96%D9%A2E%8B%16-Z*%83%96%D9%A2E%8B%16-Z%B4T%86%D9%A2E%8B%16-Z%B4T%06-%B3E%8B%16-Z%B4%AE%A4%F5%25%C0%00%DE%BF%5C'%0F%DA%B8q%00%00%00%00IEND%AEB%60%82") repeat-y !important;
    border-left: 1px solid #BBBBBB !important;
    border-right: 1px solid #000000 !important;
    border-bottom: 1px dashed #BBBBBB !important;
}

.overflowRulerX > .firebugRulerV {
    left: 0 !important;
}

.overflowRulerY > .firebugRulerH {
    top: 0 !important;
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
.fbProxyElement {
    position: fixed !important;
    pointer-events: auto !important;
}
</style></head>
<body>
	<form action="gjjbj/gjjQueryCreditAction!tzrFrame.dhtml" method="post" name="iframeFrame" id="iframeFrame">
	<input id="pageNos" name="pageNos" value="1" type="hidden">
	<input id="ent_id" name="ent_id" value="DCBB0FD56D324C87AD672F5D35EA3437" type="hidden">
	<input id="fqr" name="fqr" value="" type="hidden">
	<table class="detailsList" id="touziren" cellpadding="0" cellspacing="0">



					<tbody><tr>
						<th colspan="4" style="text-align:center;">


								股东信息<br>
								<span style="font-size:12px;">股东的出资信息截止2014年2月28日。2014年2月28日之后工商只公示股东姓名，其他出资信息由企业自行公示。</span>

						 </th>
					</tr>






		</tbody><tbody id="table2">
			<tr width="95%">


	          <th style="text-align:center;" width="10%">股东类型</th>
	          <th style="text-align:center;" width="10%">股东</th>

			  <th style="text-align:center;" width="10%">证照/证件类型</th>
			  <th style="text-align:center;" width="10%">证照/证件号码</th>



	        </tr>

	         <tr id="tr1">
	         	<td>自然人股东</td>
	         	<td>李彦宏</td>
	         	<td></td>
	         	<td></td>



	         </tr>

	         <tr id="tr1">
	         	<td>自然人股东</td>
	         	<td>王湛</td>
	         	<td></td>
	         	<td></td>



	         </tr>






						<tr><th colspan="4" style="text-align:right;"><a href="javascript:void(0)" title="上一页" style="vertical-align:bottom" onclick="jumppage('0');return false">&lt;&lt;</a>&nbsp;&nbsp;<font style="text-decoration:none;color:red">1</font>&nbsp;&nbsp;<a href="javascript:void(0)" title="下一页" style="vertical-align:bottom" onclick="jumppage('2');return false">&gt;&gt;</a>&nbsp;&nbsp;<input id="pageNo" name="pageNo" value="1" type="hidden"><input value="1" id="pagescount" type="hidden"><input id="pageSize" name="pageSize" value="5" type="hidden"><input id="clear" name="clear" type="hidden"></th></tr>






		</tbody>
	</table>
   </form>

</body></html>'''

enterprise_html_changedinfo='''
<html xmlns="http://www.w3.org/1999/xhtml"><head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet">
	<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script><!-- 1.9版本jQuery js   -->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/pubInfo.js"></script><!-- 北京首页pubInfo.js js   -->
	<script type="text/javascript" src="/js/ajax/http.js"></script>
	<script type="text/javascript">
	var rootPath = '';
 	var entId = 'DCBB0FD56D324C87AD672F5D35EA3437';
	var entName = '北京百度网讯科技有限公司';
	var entNo = '';
	</script>
	<style>
	html { overflow:hidden; }
	</style>
</head>
<body>
	<form action="gjjbj/gjjQueryCreditAction!biangengFrame.dhtml" method="post" name="iframeFrame" id="iframeFrame">
	<input id="pageNos" name="pageNos" value="1" type="hidden">
	<input id="ent_id" name="ent_id" value="DCBB0FD56D324C87AD672F5D35EA3437" type="hidden">
	<table class="detailsList" id="touziren" cellpadding="0" cellspacing="0">
		<tbody id="table2">
			<tr width="95%"><th colspan="4" style="text-align:center;">变更信息</th></tr>
			<tr width="95%">
			<th style="text-align:center;" width="15%"> 变更事项</th>
			<th style="text-align:center;" width="25%"> 变更前内容</th>
			<th style="text-align:center;" width="25%"> 变更后内容</th>
			<th style="text-align:center;" width="10%"> 变更日期</th>
			</tr>



	         <tr id="tr1">
	         	<td>经营范围</td>

	         		<td>因特信息服务业务（除出版、教育、医疗保健以外的内容）；第一类增值电信业务中的在线数据处理与交易处理业务、国内因特网虚拟专用网业务、因特网数据中心业务；第二类增值电信业务中的因特网接入服务业务、呼叫中心业务、信息服务业务（不含固定网电话信息服务和互联网信息服务）（增值电信业务经营许可证有效期至2015年10月20日）；利用互联网经营音乐娱乐产品，游戏产品运营，网络游戏虚拟货币发行，美术品，演出剧（节）目，动漫（画）产品，从事互联网文化产品展览、比赛活动（网络文化经营许可证有效期至2016年11月21日）；设计、开发、销售计算机软件；技术服务、技术培训、技术推广；经济信息咨询；利用www.baidu.com、www.hao123.com(www.hao222.net、www.hao222.com)、网站发布广告；设计、制作、代理、发布广告；货物进出口、技术进出口、代理进出口；医疗软件技术开发；健康咨询（须经审批的诊疗活动除外）；委托生产电子产品、玩具、照相器材；销售家用电器、机械设备、五金交电、电子产品、文化用品、照相器材、计算机、软件及辅助设备、化妆品、卫生用品、体育用品、纺织品、服装、鞋帽、日用品、家具、首饰、避孕器具、工艺品、钟表、眼镜、玩具、汽车及摩托车配件、仪器仪表、塑料制品、花、草及观赏植物、建筑材料、通讯设备。</td>
		         	<td>因特信息服务业务（除出版、教育、医疗保健以外的内容）；第一类增值电信业务中的在线数据处理与交易处理业务、国内因特网虚拟专用网业务、因特网数据中心业务；第二类增值电信业务中的因特网接入服务业务、呼叫中心业务、信息服务业务（不含固定网电话信息服务和互联网信息服务）（增值电信业务经营许可证有效期至2015年10月20日）；利用互联网经营音乐娱乐产品，游戏产品运营，网络游戏虚拟货币发行，美术品，演出剧（节）目，动漫（画）产品，从事互联网文化产品展览、比赛活动（网络文化经营许可证有效期至2016年11月21日）；设计、开发、销售计算机软件；技术服务、技术培训、技术推广；经济信息咨询；利用www.baidu.com、www.hao123.com(www.hao222.net、www.hao222.com)、网站发布广告；设计、制作、代理、发布广告；货物进出口、技术进出口、代理进出口；医疗软件技术开发；委托生产电子产品、玩具、照相器材；销售家用电器、机械设备、五金交电、电子产品、文化用品、照相器材、计算机、软件及辅助设备、化妆品、卫生用品、体育用品、纺织品、服装、鞋帽、日用品、家具、首饰、避孕器具、工艺品、钟表、眼镜、玩具、汽车及摩托车配件、仪器仪表、塑料制品、花、草及观赏植物、建筑材料、通讯设备；预防保健咨询。依法须经批准的项目，经相关部门批准后依批准内容开展经营活动。</td>


	         	<td>2015-01-12</td>
	         </tr>

	         <tr id="tr1">
	         	<td>经营范围</td>

	         		<td>因特信息服务业务（除出版、教育、医疗保健以外的内容）；第一类增值电信业务中的在线数据处理与交易处理业务、国内因特网虚拟专用网业务、因特网数据中心业务；第二类增值电信业务中的因特网接入服务业务、呼叫中心业务、信息服务业务（不含固定网电话信息服务和互联网信息服务）（增值电信业务经营许可证有效期至2015年10月20日）；利用互联网经营音乐娱乐产品，游戏产品运营，网络游戏虚拟货币发行，美术品，演出剧（节）目，动漫（画）产品，从事互联网文化产品展览、比赛活动（网络文化经营许可证有效期至2016年11月21日）；设计、开发、销售计算机软件；技术服务、技术培训、技术推广；经济信息咨询；利用www.baidu.com、www.hao123.com(www.hao222.net、www.hao222.com)、网站发布广告；设计、制作、代理、发布广告；货物进出口、技术进出口、代理进出口；医疗软件技术开发。</td>
		         	<td>因特信息服务业务（除出版、教育、医疗保健以外的内容）；第一类增值电信业务中的在线数据处理与交易处理业务、国内因特网虚拟专用网业务、因特网数据中心业务；第二类增值电信业务中的因特网接入服务业务、呼叫中心业务、信息服务业务（不含固定网电话信息服务和互联网信息服务）（增值电信业务经营许可证有效期至2015年10月20日）；利用互联网经营音乐娱乐产品，游戏产品运营，网络游戏虚拟货币发行，美术品，演出剧（节）目，动漫（画）产品，从事互联网文化产品展览、比赛活动（网络文化经营许可证有效期至2016年11月21日）；设计、开发、销售计算机软件；技术服务、技术培训、技术推广；经济信息咨询；利用www.baidu.com、www.hao123.com(www.hao222.net、www.hao222.com)、网站发布广告；设计、制作、代理、发布广告；货物进出口、技术进出口、代理进出口；医疗软件技术开发；健康咨询（须经审批的诊疗活动除外）；委托生产电子产品、玩具、照相器材；销售家用电器、机械设备、五金交电、电子产品、文化用品、照相器材、计算机、软件及辅助设备、化妆品、卫生用品、体育用品、纺织品、服装、鞋帽、日用品、家具、首饰、避孕器具、工艺品、钟表、眼镜、玩具、汽车及摩托车配件、仪器仪表、塑料制品、花、草及观赏植物、建筑材料、通讯设备。</td>


	         	<td>2014-12-25</td>
	         </tr>

	         <tr id="tr1">
	         	<td>经营范围</td>

	         		<td>因特信息服务业务（除出版、教育、医疗保健以外的内容）；第二类增值电信业务中的呼叫中心业务和信息服务业务（不含固定网电话信息服务和互联网信息服务）；利用互联网经营音乐娱乐产品，游戏产品运营，网络游戏虚拟货币发行，美术品，演出剧（节）目，动漫（画）产品，从事互联网文化产品展览、比赛活动。（网络文化经营许可证有效期至2013年12月31日）设计、开发、销售计算机软件；技术服务、技术培训、技术推广；经济信息咨询；利用www.baidu.com、www.hao123.com(www.hao222.net、www.hao222.com)、www.youa.com(www.youa.com.cn、www.youa.cn)网站发布广告；设计、制作、代理、发布广告；货物进出口、技术进出口、代理进出口。</td>
		         	<td>因特信息服务业务（除出版、教育、医疗保健以外的内容）；第一类增值电信业务中的在线数据处理与交易处理业务、国内因特网虚拟专用网业务、因特网数据中心业务；第二类增值电信业务中的因特网接入服务业务、呼叫中心业务、信息服务业务（不含固定网电话信息服务和互联网信息服务）（增值电信业务经营许可证有效期至2015年10月20日）；利用互联网经营音乐娱乐产品，游戏产品运营，网络游戏虚拟货币发行，美术品，演出剧（节）目，动漫（画）产品，从事互联网文化产品展览、比赛活动（网络文化经营许可证有效期至2016年11月21日）；设计、开发、销售计算机软件；技术服务、技术培训、技术推广；经济信息咨询；利用www.baidu.com、www.hao123.com(www.hao222.net、www.hao222.com)、网站发布广告；设计、制作、代理、发布广告；货物进出口、技术进出口、代理进出口；医疗软件技术开发。</td>


	         	<td>2014-11-05</td>
	         </tr>






				<tr>
					<th colspan="4" style="text-align:right;">
					<a href="javascript:void(0)" title="上一页" style="vertical-align:bottom" onclick="jumppage('0');return false">&lt;&lt;</a>&nbsp;&nbsp;<a href="javascript:void(0)" onclick="jumppage('1');return false"><font style="text-decoration:none;color:red">1</font></a>&nbsp;&nbsp;<a href="javascript:void(0)" title="下一页" style="vertical-align:bottom" onclick="jumppage('2');return false">&gt;&gt;</a>&nbsp;&nbsp;<input id="pageNo" name="pageNo" value="1" type="hidden"><input value="1" id="pagescount" type="hidden"><input id="pageSize" name="pageSize" value="5" type="hidden"><input id="clear" name="clear" type="hidden">
				</th>
				</tr>

		</tbody>
	</table>
   </form>

</body></html>'''


enterprise_html_key_member='''
<html xmlns="http://www.w3.org/1999/xhtml"><head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet">
	<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script><!-- 1.9版本jQuery js   -->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/pubInfo.js"></script><!-- 北京首页pubInfo.js js   -->
	<script type="text/javascript">
	var rootPath = '';
 	var entId = 'DCBB0FD56D324C87AD672F5D35EA3437';
	var entName = '';
	var entNo = '';

	</script>
	<style>
	html { overflow:hidden; }
	</style>
</head>
<body>
	<form action="gjjbj/gjjQueryCreditAction!zyryFrame.dhtml" method="post" name="iframeFrame" id="iframeFrame">
	<input id="pageNos" name="pageNos" value="1" type="hidden">
	<input id="ent_id" name="ent_id" value="DCBB0FD56D324C87AD672F5D35EA3437" type="hidden">
	<table class="detailsList" id="touziren" cellpadding="0" cellspacing="0">
		<tbody id="table2">
			<tr width="95%">
				<th colspan="6" style="text-align:center;">主要人员信息</th>
			</tr>
			<tr>
				<th style="width:10%;text-align:center">序号</th>
				<th style="width:20%;text-align:center">姓名</th>
				<th style="width:20%;text-align:center">职务</th>
				<th style="width:10%;text-align:center">序号</th>
				<th style="width:20%;text-align:center">姓名</th>
				<th style="width:20%;text-align:center">职务</th>
	        </tr>

	        	<tr>
		         	<td style="text-align:center;">1</td>
		         	<td>李彦宏</td>
		         	<td>执行董事</td>



		         	<td style="text-align:center;">2</td>
		         	<td>梁志祥</td>
		         	<td>总经理</td>
		         </tr>



				<tr>
					<th colspan="6" style="text-align:right;">
						<a href="javascript:void(0)" title="上一页" style="vertical-align:bottom" onclick="jumppage('0');return false">&lt;&lt;</a>&nbsp;&nbsp;<font style="text-decoration:none;color:red">1</font>&nbsp;&nbsp;<a href="javascript:void(0)" title="下一页" style="vertical-align:bottom" onclick="jumppage('2');return false">&gt;&gt;</a>&nbsp;&nbsp;<input id="pageNo" name="pageNo" value="1" type="hidden"><input value="1" id="pagescount" type="hidden"><input id="pageSize" name="pageSize" value="10" type="hidden"><input id="clear" name="clear" type="hidden">
					</th>
				</tr>

		</tbody>
	</table>
   </form>

</body></html>
'''

enterprise_html_xizang = '''

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <META HTTP-EQUIV="pragma" CONTENT="no-cache"/>
    <META HTTP-EQUIV="Cache-Control" CONTENT="no-cache, must-revalidate"/>
    <META HTTP-EQUIV="expires" CONTENT="Wed, 26 Feb 1997 08:21:57 GMT"/>
    <title>全国企业信用信息公示系统</title>
    <link href="/css/public3.css" type="text/css" rel="stylesheet"/>
    <script type="text/javascript" src="/js/ajax.js"></script>
    <script type="text/javascript" src="/js/infoExpand.js"></script>
	<script type="text/javascript">
		function closephone(){
			document.getElementById('sxphone').style.display='none';
			document.getElementById('bgDiv').style.display='none';
		}
		function iframeLoad(){
			var sxphoneHeight=$('#sxphone').height();
			$('#phoneiframe').height(sxphoneHeight-40);
		}
		function openphone(){
			window.scrollTo(0,0);
				var winWidth = 0;
		        var winHeight = 0;
		        if (window.innerWidth)
		              winWidth = window.innerWidth;
		        else if ((document.body) && (document.body.clientWidth))
		              winWidth = document.body.clientWidth;
		        //获取窗口高度
		        if (window.innerHeight)
		              winHeight = window.innerHeight;
		        else if ((document.body) && (document.body.clientHeight))
		              winHeight = document.body.clientHeight;

			var sxphone=document.getElementById("sxphone");
			if(sxphone){
				sxphone.top="50%";
				sxphone.left="50%";
				 //获取窗口宽度
				sxphone.style.display="";
				document.getElementById('bgDiv').style.display='';
			}
			else{
			 	var bgObj =document.createElement("div");
			    bgObj.setAttribute('id','bgDiv');
			    bgObj.style.position="absolute";
			    bgObj.style.top="0";
			    bgObj.style.background="#777";
			    bgObj.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75";
			    bgObj.style.opacity="0.6";
			    bgObj.style.left="0";
			    bgObj.style.width=winWidth + "px";
			    bgObj.style.height=winHeight + "px";
			    bgObj.style.zIndex = "1000";
			    bgObj.style.MozOpacity="0.7";

			    document.body.appendChild(bgObj);
				var div = document.createElement("div");
				//div.id="sxphone";
				div.setAttribute('id','sxphone');
				div.style.height="80%";
				div.style.width="800px";
				div.style.border="0px solid red";
				div.style.position="absolute";
				div.style.left="50%";
				div.style.margin="0 0 0 -400px";
				div.style.top="5%";
				div.style.zIndex = "10001";
				div.style.MozBorderRadius="5px";
				div.style.webkitBorderRadius="5px";
				div.style.borderRadius="5px";
				div.style.background="#2D84B2";
				div.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=100,finishOpacity=100";
				div.style.padding="0";
				  div.style.MozOpacity="1";
				div.innerHTML = "<div style='font-weight: bold;color: #fff;height:20px;padding:5px 20px;font-size:14px'><img src='/js/skins/ZCMS/images/icon.gif'/>咨询电话<span style='float:right;'>"+
				"<a style='color:#fff;font-size:12px' href='javascript:closephone();' title='关闭'>关闭</a></span></div>"+
					"<iframe id='phoneiframe' src='/sxphone.jspx' style='width:790px;border:0px solid red;padding:0;margin:5px 5px -10px 5px;' onload='iframeLoad()'></iframe>";
				document.body.appendChild(div);
				var ua = navigator.userAgent;
			    if (ua.lastIndexOf("MSIE 6.0") != -1) {
			    	var phoneiframe=document.getElementById("phoneiframe");
			    	//phoneiframe.style.width="840px";
			    	phoneiframe.style.height="580px";
			    	phoneiframe.style.marginRight="-15px";
				}
			}
		}
		function iframeLoadHb(){
			var sxphoneHeight=$('#sxphone').height();
			$('#phoneiframe').height(sxphoneHeight-60);
		}
			function openphonehb(){
			window.scrollTo(0,0);
				var winWidth = 0;
		        var winHeight = 0;
		        if (window.innerWidth)
		              winWidth = window.innerWidth;
		        else if ((document.body) && (document.body.clientWidth))
		              winWidth = document.body.clientWidth;
		        //获取窗口高度
		        if (window.innerHeight)
		              winHeight = window.innerHeight;
		        else if ((document.body) && (document.body.clientHeight))
		              winHeight = document.body.clientHeight;

			var sxphone=document.getElementById("sxphone");
			if(sxphone){
				sxphone.top="50%";
				sxphone.left="50%";
				 //获取窗口宽度
				sxphone.style.display="";
				document.getElementById('bgDiv').style.display='';
			}
			else{
			 	var bgObj =document.createElement("div");
			    bgObj.setAttribute('id','bgDiv');
			    bgObj.style.position="absolute";
			    bgObj.style.top="0";
			    bgObj.style.background="#777";
			    bgObj.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75";
			    bgObj.style.opacity="0.6";
			    bgObj.style.left="0";
			    bgObj.style.width=winWidth + "px";
			    bgObj.style.height=winHeight + "px";
			    bgObj.style.zIndex = "1000";
			    bgObj.style.MozOpacity="0.7";

			    document.body.appendChild(bgObj);
				var div = document.createElement("div");
				//div.id="sxphone";
				div.setAttribute('id','sxphone');
				div.style.height="80%";
				div.style.width="800px";
				div.style.border="0px solid red";
				div.style.position="absolute";
				div.style.left="50%";
				div.style.margin="0 0 0 -400px";
				div.style.top="5%";
				div.style.zIndex = "10001";
				div.style.background="#ECEEEE";
				div.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=100,finishOpacity=100";
				div.style.padding="0";
				  div.style.MozOpacity="1";
				div.innerHTML = "<div style='font-weight: bold;color: #000;height:20px;padding:5px 20px;font-size:14px;'>咨询电话<span style='float:right;'>"+
				"<a style='color:#000;font-size:12px' href='javascript:closephone();' title='关闭'>关闭</a></span></div>"+
				"<hr />"+
					"<iframe id='phoneiframe' src='/hbphone.jspx' style='width:790px;border:0px solid red;padding:0;margin:5px 5px -10px 5px;' onload='iframeLoadHb()'></iframe>";
				document.body.appendChild(div);
				var ua = navigator.userAgent;
			    if (ua.lastIndexOf("MSIE 6.0") != -1) {
			    	var phoneiframe=document.getElementById("phoneiframe");
			    	//phoneiframe.style.width="840px";
			    	phoneiframe.style.height="580px";
			    	phoneiframe.style.marginRight="-15px";
				}
			}
		}
	</script>
    <script type="text/javascript">
        function r1() {
            document.getElementById('jibenxinxi').style.display = 'block';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';

        }
        function r2() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'block';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';

        }
        function r3() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'block';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';

        }
        function r4() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'block';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';
        }
        function r5() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'block';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';
        }
        function r6() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'block';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';
        }
        function r7() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'block';
            document.getElementById('chouchaxinxi').style.display = 'none';
        }
        function r8() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'block';
        }

        function togo(str) {
            if (str == '1') {
                window.location = '/businessPublicity.jspx?id=C0E2ED0898EBC82FD7567EC589AC9776';
            } else if (str == '2') {
                window.location = '/enterprisePublicity.jspx?id=C0E2ED0898EBC82FD7567EC589AC9776';
            }else if (str == '3') {
                window.location = '/otherDepartment.jspx?id=C0E2ED0898EBC82FD7567EC589AC9776';
            }else if(str == '4'){
                window.location = '/justiceAssistance.jspx?id=C0E2ED0898EBC82FD7567EC589AC9776';
            }
        }
          function changeTab() {
                var sourType = "";
                   if (sourType == "1") {
                    r5();
                    var tab = document.getElementById("5");
                    changeStyle('tabs',tab);
                  } else if (sourType == "2") {
                    r6();
                    var tab = document.getElementById("6");
                    changeStyle('tabs',tab);
                  } else if (sourType == "3") {
                    r8();
                    var tab = document.getElementById("8");
                    changeStyle('tabs',tab);
                  }
        }
        window.onload = function() {
              changeTab();
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

                }
                else {
                    liAry[i].className = "";
                }
            }
        }

        function ShowSpan(obj, n) {
            var span = obj.parentNode.getElementsByTagName("tabs");
            for (var i = 0; i < span.length; i++) {
                span[i].className = "current";
            }
            span[n].className = "";
            var li = obj.parentNode.getElementsByTagName("li")
            li[n].className = "current";
            for (var i = 0; i < li.length; i++) {
                if (i != n) {
                    li[i].className = "";
                }
                li[i].onmouseout = function () {
                    this.className = "current";
                }
            }
        }
    </script>

</head>
<style type="text/css">
    th,td{word-break:break-all;}
  .top{width:990px; height:124px; background:url("/images/xizang.png") no-repeat; }
  .banqun{width:990px; height:59px; bottom:0; background:url("/images/ban-bj.png") repeat-x  ; padding-top:20px;font-size:14px; text-align:center; margin:0 auto;color:#fff;font-family:"微软雅黑";clear:both;}
</style>

<body>
<div id="header">
    <div class="top">
        <div class="top-a">
		<a href="http://gsxt.saic.gov.cn"  style="font-size:14px ; font-family:'微软雅黑'">全国首页</a>&nbsp;&nbsp;<a href="/search.jspx"
		style="font-size:14px ; font-family:'微软雅黑'">地方局首页</a>
        </div>
    </div>
</div>
<br><br><br><br>

<div id="details" class="clear" style="min-height: 880px;height: auto;">

    <h2 >
         西藏城市发展投资股份有限公司 &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp; 注册号/统一社会信用代码：540000100003419&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;
    </h2>

<br/>

<div id="leftTabs">
    <ul>
        <li class="current" style="margin-bottom:2px;"><p>工<br/>商<br/>公<br/>示<br/>信<br/>息</p></li>
        <li onclick="togo('2')" style="margin-bottom:2px;"><p>企<br/>业<br/>公<br/>示<br/>信<br/>息</p></li>
        <li onclick="togo('3')" style="margin-bottom:2px;"><p>其<br/>他<br/>部<br/>门<br/>公<br/>示<br/>信<br/>息</p></li>
        <li onclick="togo('4')"  style="margin-bottom:2px;"><p>司<br/>法<br/>协<br/>助<br/>公<br/>示<br/>信<br/>息</p></li>
    </ul>
</div>
<div id="detailsCon" style="height:1038px;overflow:atuo">
<div class="dConBox">
<div class="tabs" id="tabs">
    <ul>
        <li id="1" class="current" onclick="r1(),changeStyle('tabs',this)">登记信息</li>
        <li id="2" onclick="r2(),changeStyle('tabs',this)">备案信息</li>
        <li id="4" onclick="r4(),changeStyle('tabs',this)">动产抵押登记信息</li>
        <li id="3" onclick="r3(),changeStyle('tabs',this)">股权出质登记信息</li>
        <li id="7" onclick="r7(),changeStyle('tabs',this)">行政处罚信息</li>
        <li id="5" onclick="r5(),changeStyle('tabs',this)">经营异常信息</li>
        <li id="6" onclick="r6(),changeStyle('tabs',this)">严重违法信息</li>
        <li id="8" onclick="r8(),changeStyle('tabs',this)">抽查检查信息</li>
    </ul>
</div>

<div id="jibenxinxi" style="height: 850px;width:930px;overflow: auto">
    </br>
    <table cellspacing="0" cellpadding="0" class="detailsList">
        <tr>
            <th colspan="4" style="text-align:center;">基本信息</th>
        </tr>

        <tr>
        <th width="20%">注册号/统一社会信用代码</th>
        <td width="30%"> 540000100003419 </td>
        <th>名称</th>
        <td width="30%">西藏城市发展投资股份有限公司</td>
    </tr>
        <tr>
            <th>类型</th>
            <td>股份有限公司（上市、外商投资企业投资）</td>
            <th width="20%">法定代表人</th>
            <td>朱贤麟</td>
        </tr>
        <tr>
            <th>注册资本</th>
            <td>72,921.3663万元</td>
            <th width="20%">成立日期</th>
            <td>
                    1996年10月25日
            </td>

        </tr>
        <tr>
            <th>住所</th>
            <td colspan="3">
                西藏自治区拉萨市金珠西路75号2楼
            </td>
        </tr>
        <tr>
            <th>营业期限自</th>
            <td>
                    1996年10月25日
            </td>
            <th>营业期限至</th>
            <td>
                    2156年10月25日
            </td>
        </tr>
        <tr>
            <th>经营范围<br/></th>
            <td colspan="3">
                一般经营项目：对矿业、金融、实业的投资；（不具体从事以上经营项目）。建材销售；建筑工程咨询。（经营项目涉及行政许可的，凭行政许可证或审批文件经营）
            </td>
        </tr>
        <tr>
            <th>登记机关</th>
            <td>西藏自治区工商行政管理局</td>
            <th>核准日期</th>
            <td>
                    2015年1月23日
            </td>
        </tr>
        <tr>
            <th>登记状态</th>
            <td>存续</td>
            <th></th>
            <td></td>

        </tr>

    </table>
    <br>
    <table cellspacing="0" cellpadding="0" class="detailsList" id="touziren">
        <tr>
            <th colspan="5" style="text-align:center;">股东（发起人）信息<br/>
                <span style="font-weight:normal">股东（发起人）的出资信息截止2014年2月28日。2014年2月28日之后工商只公示股东（发起人）姓名，其他出资信息由企业自行公示。</span></th>
        </tr>
        <tr width="95%">
            <th width="20%" style="text-align:center;">股东（发起人）</th>
            <th width="20%" style="text-align:center;">证照/证件类型</th>
            <th width="20%" style="text-align:center;">证照/证件号码</th>
            <th width="20%" style="text-align:center;">股东（发起人）类型</th>
            <th width="20%" style="text-align:center;">详情</th>
        </tr>
    </table>
    <div id="invDiv">
        <table cellspacing="0" cellpadding="0" class="detailsList">
                    <tr>
                          <td width="20%">
                            社会公众股
                        </td>
                         <td width="20%">
                                    其他
                        </td>
                        <td width="20%">

                        </td>
                         <td width="20%">
                            其他投资者
                        </td>
                        <td width="20%">
                            <a href="javascript:void(0)" onclick="window.open('/queryInvDetailAction.jspx?id=154000000202443875')">详情</a>
                        </td>
                    </tr>
                    <tr>
                          <td width="20%">
                            社会公众股东
                        </td>
                         <td width="20%">
                                    内资企业法人
                        </td>
                        <td width="20%">

                        </td>
                         <td width="20%">
                            企业法人
                        </td>
                        <td width="20%">
                            <a href="javascript:void(0)" onclick="window.open('/queryInvDetailAction.jspx?id=154000000202219359')">详情</a>
                        </td>
                    </tr>
                    <tr>
                          <td width="20%">
                            西藏自治区包装进出口公司
                        </td>
                         <td width="20%">
                                    内资企业法人
                        </td>
                        <td width="20%">
                                    5400001000164
                        </td>
                         <td width="20%">
                            企业法人
                        </td>
                        <td width="20%">
                            <a href="javascript:void(0)" onclick="window.open('/queryInvDetailAction.jspx?id=154000000202219361')">详情</a>
                        </td>
                    </tr>
                    <tr>
                          <td width="20%">
                            西藏自治区信托投资公司
                        </td>
                         <td width="20%">
                                    内资企业法人
                        </td>
                        <td width="20%">
                                    5400001600123
                        </td>
                         <td width="20%">
                            企业法人
                        </td>
                        <td width="20%">
                            <a href="javascript:void(0)" onclick="window.open('/queryInvDetailAction.jspx?id=154000000202219363')">详情</a>
                        </td>
                    </tr>
                    <tr>
                          <td width="20%">
                            北京新联金达投资有限公司
                        </td>
                         <td width="20%">
                                    内资企业法人
                        </td>
                        <td width="20%">
                                    110000008133597
                        </td>
                         <td width="20%">
                            企业法人
                        </td>
                        <td width="20%">
                            <a href="javascript:void(0)" onclick="window.open('/queryInvDetailAction.jspx?id=154000000202219365')">详情</a>
                        </td>
                    </tr>
        </table>
    </div>
            <table cellpadding="0" cellspacing="0" class="detailsList">
                <th colspan="4" style="text-align:right;">
                    <span style="color:blue"><<</span>
                        &nbsp;<a id="ainv1" href='javascript:goPage3("inv",1);' style="text-decoration:none"><span id="spaninv1" style="color:red">1</span></a>
	                                                        &nbsp;<a id="ainv2" href='javascript:goPage3("inv",2);'><span id="spaninv2">2</span></a>
                    &nbsp;<span style="color:blue">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
            </table>

    </br>


    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="4" style="text-align:center;">变更信息</th>
        </tr>
        <tr width="95%">
            <th width="15%" style="text-align:center;"> 变更事项</th>
            <th width="25%" style="text-align:center;"> 变更前内容</th>
            <th width="25%" style="text-align:center;"> 变更后内容</th>
            <th width="10%" style="text-align:center;"> 变更日期</th>
        </tr>
    </table>
    <div id="altDiv">
        <table cellspacing="0" cellpadding="0" class="detailsList" id="altTab">
                    <tr width="95%">
                        <td width="15%">实收资本(或外资中方实收资本)</td>
                        <td width="25%">57570.4998</td>
                        <td width="25%">72921.366300</td>
                        <td width="10%" style="text-align:center">
                            2015年1月23日
                        </td>
                    </tr>
                    <tr width="95%">
                        <td width="15%">注册资本(或外资中方认缴资本)</td>
                        <td width="25%">57570.4998</td>
                        <td width="25%">72921.366300</td>
                        <td width="10%" style="text-align:center">
                            2015年1月23日
                        </td>
                    </tr>
                    <tr width="95%">
                        <td width="15%">股东、发起人（出资情况）</td>
                        <td width="25%">社会公众股东;西藏自治区包装进出口公司;西藏自治区信托投资公司;北京新联金达投资有限公司;南京长恒实业有限公司;中国出口商品基地建设西藏分公司;西藏国际经济技术合作公司;江苏中桥百合通讯产品销售有限公司;上海市闸北区国有资产监督管理委员会;</td>
                        <td width="25%">北京新联金达投资有限公司;社会公众股东;西藏自治区包装进出口公司;西藏自治区信托投资公司;上海市闸北区国有资产监督管理委员会;南京长恒实业有限公司;中国出口商品基地建设西藏分公司;西藏国际经济技术合作公司;江苏中桥百合通讯产品销售有限公司;社会公众股;</td>
                        <td width="10%" style="text-align:center">
                            2015年1月23日
                        </td>
                    </tr>
        </table>
    </div>
            <table cellpadding="0" cellspacing="0" class="detailsList">
                <th colspan="4" style="text-align:right;">
                    <span style="color:blue"><<</span>
                        &nbsp;<a id="aalt1" href='javascript:goPage3("alt",1);' style="text-decoration:none"><span id="spanalt1" style="color:red">1</span></a>
                                                        &nbsp;<span style="color:blue">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
            </table>

</div>


<div id="beian" style="align:center;display:none;height: 850px;width:930px;overflow: auto">
    <br>
    <table style="width:100%;" id="t30" cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="939px">
            <th colspan="6" style="text-align:center;">主要人员信息</th>
        </tr>
        <th style="width:10%;text-align:center">序号</th>
        <th style="width:20%;text-align:center">姓名</th>
        <th style="width:20%;text-align:center">职务</th>
        <th style="width:10%;text-align:center">序号</th>
        <th style="width:20%;text-align:center">姓名</th>
        <th style="width:20%;text-align:center">职务</th>
        </tr>
    </table>
    <div id="memDiv">
        <table cellspacing="0" cellpadding="0" class="detailsList">
                        <tr>
                    <td style="width:10%;text-align:center">1</td>
                    <td style="width:20%">朱贤麟                        </td>
                    <td style="width:20%">董事长</td>

                    <td style="width:10%;text-align:center">2</td>
                    <td style="width:20%">陈卫东                        </td>
                    <td style="width:20%">董事</td>
                        </tr>

                        <tr>
                    <td style="width:10%;text-align:center">3</td>
                    <td style="width:20%">吴素芬                        </td>
                    <td style="width:20%">监事</td>

                    <td style="width:10%;text-align:center">4</td>
                    <td style="width:20%">颜学海                        </td>
                    <td style="width:20%">董事</td>
                        </tr>

                        <tr>
                    <td style="width:10%;text-align:center">5</td>
                    <td style="width:20%">董惠良                        </td>
                    <td style="width:20%">董事</td>

                    <td style="width:10%;text-align:center">6</td>
                    <td style="width:20%">王列新                        </td>
                    <td style="width:20%">监事</td>
                        </tr>

                        <tr>
                    <td style="width:10%;text-align:center">7</td>
                    <td style="width:20%">唐泽平                        </td>
                    <td style="width:20%">董事</td>

                    <td style="width:10%;text-align:center">8</td>
                    <td style="width:20%">曾云                          </td>
                    <td style="width:20%">董事</td>
                        </tr>

                        <tr>
                    <td style="width:10%;text-align:center">9</td>
                    <td style="width:20%">华伟                          </td>
                    <td style="width:20%">董事</td>

                    <td style="width:10%"></td><td style="width:20%"></td><td style="width:20%"></td></tr>
        </table>
    </div>
            <table cellpadding="0" cellspacing="0" class="detailsList">
                <th colspan="4" style="text-align:right;">
                    <span style="color:blue"><<</span>
                        &nbsp;<a id="amem1" href='javascript:goPage3("mem",1);' style="text-decoration:none"><span id="spanmem1" style="color:red">1</span></a>
                                                        &nbsp;<span style="color:blue">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
            </table>

    </br>

    <br>

    <table id="t31" cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="939px">
            <th colspan="4" style="text-align:center;">分支机构信息</th>
        </tr>
        <tr>
            <th style="text-align:center;width:10%;">序号</th>
            <th style="text-align:center;width:25%">注册号/统一社会信用代码</th>
            <th style="text-align:center;width:25%">名称</th>
            <th style="text-align:center;width:20%">登记机关</th>
        </tr>
    </table>
    <div id="childDiv">
        <table cellspacing="0" cellpadding="0" class="detailsList">
        </table>
    </div>

    <br>


    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="939px">
            <th colspan="5" style="text-align:center;">清算信息</th>
        </tr>
        <tr>
            <th style="width:20%">清算组负责人</th>
            <td colspan="4">


            </td>
        </tr>
        <tr>
            <th rowspan="">清算组成员 </th>
            <td colspan="4">
            </td>
        </tr>
    </table>
</div>

<div id="guquanchuzhi" style="display:none;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="11" style="text-align:center;">股权出质登记信息</th>
        </tr>
        <tr width="95%">
            <th width="5%" style="text-align:center;">序号</th>
            <th width="8%" style="text-align:center;">登记编号</th>
            <th width="6%" style="text-align:center;">出质人</th>
            <th width="13%" style="text-align:center;">证照/证件号码</th>
            <th width="8%" style="text-align:center;">出质股权数额</th>
            <th width="8%" style="text-align:center;">质权人</th>
            <th width="13%" style="text-align:center;">证照/证件号码</th>
            <th width="12%" style="text-align:center;">股权出质设立登记日期</th>
            <th width="7%" style="text-align:center;">状态</th>
            <th width="11%" style="text-align:center">公示日期</th>
            <th width="6%" style="text-align:center;">变化情况</th>
        </tr>
    </table>

    <div id="pledgeDiv">
        <table cellpadding="0" cellspacing="0" class="detailsList">
        </table>
    </div>

    <br/>
</div>

<div id="dongchandiya" style="display:none ;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="9" style="text-align:center;">动产抵押登记信息</th>
        </tr>
        <tr width="95%">
            <th width="5%" style="text-align:center;">序号</th>
            <th width="20%" style="text-align:center;">登记编号</th>
            <th width="12%" style="text-align:center;">登记日期</th>
            <th width="20%" style="text-align:center;">登记机关</th>
            <th width="15%" style="text-align:center;">被担保债权数额</th>
            <th width="7%" style="text-align:center;">状态</th>
            <th width="13%" style="text-align:center;">公示日期</th>
            <th width="10%" style="text-align:center;">详情</th>
        </tr>
    </table>

    <div id="mortDiv">
        <table cellpadding="0" cellspacing="0" class="detailsList">
    </table>
    </div>
    <br/>
</div>

<div id="jingyingyichangminglu" style="display:none;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="6" style="text-align:center;">经营异常信息</th>
        </tr>
        <tr width="95%">
            <th width="5%" style="text-align:center;">序号</th>
            <th width="20%" style="text-align:center;">列入经营异常名录原因</th>
            <th width="13%" style="text-align:center;">列入日期</th>
            <th width="25%" style="text-align:center;">移出经营异常名录原因</th>
            <th width="13%" style="text-align:center;">移出日期</th>
            <!--<th width="13%" style="text-align:center;">公示日期</th>-->
            <th width="19%" style="text-align:center;">作出决定机关</th>
        </tr>
    </table>
    <div id="excDiv">
        <table cellspacing="0" cellpadding="0" class="detailsList" id="excTab">
                <tr>
                   <td width="5%" style="text-align:center;">1</td>
                    <td width="20%">未在工商行政管理部门依照《企业信息公示暂行条例》第十条规定责令的期限内公示有关企业信息的</td>
                    <td width="13%" style="text-align:center">
                        2015年4月7日
                    </td>
                    <td width="25%">列入经营异常名录3年内且依照《经营异常名录管理办法》第七条规定被列入经营异常名录的企业履行公示义务后，申请移出</td>
                    <td width="13%" style="text-align:center">
                        2015年7月16日
                    </td>
                    <!--<td width="13%" style="text-align:center">-->
                           <!---->
                        <!--</td>-->
                    <td width="19%">西藏自治区工商行政管理局</td>
                </tr>

    </table>
    </div>
            <table cellpadding="0" cellspacing="0" class="detailsList">
                <th colspan="4" style="text-align:right;">
                    <span style="color:blue"><<</span>
                        &nbsp;<a id="aexc1" href='javascript:goPage6("exc",1);' style="text-decoration:none"><span id="spanexc1" style="color:red">1</span></a>
                                                        &nbsp;<span style="color:blue">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
            </table>

    <br/>
</div>

<div id="yanzhongweifaqiye" style="display:none;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="6" style="text-align:center;">严重违法信息</th>
        </tr>
        <tr width="95%">
            <th width="5%" style="text-align:center;">序号</th>
            <th width="15%" style="text-align:center;">列入严重违法企业名单原因</th>
            <th width="13%" style="text-align:center;">列入日期</th>
            <th width="20%" style="text-align:center;">移出严重违法企业名单原因</th>
            <th width="13%" style="text-align:center;">移出日期</th>
            <!--<th width="13%" style="text-align:center;">公示日期</th>-->
            <th width="23%" style="text-align:center;">作出决定机关</th>
        </tr>
    </table>
    <div id="serillDiv">
    <table cellpadding="0" cellspacing="0" class="detailsList">
     </table>
     </div>
    <br/>
</div>

<div id="xingzhengchufa" style="display:none;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="9" style="text-align:center;">行政处罚信息</th>
        </tr>
        <tr width="95%">
            <th width="5%"  style="text-align:center;">序号</th>
            <th width="10%" style="text-align:center;">行政处罚<br>决定书文号</th>
            <th width="20%" style="text-align:center;">违法行为类型</th>
            <th width="18%" style="text-align:center;">行政处罚内容</th>
            <th width="18%" style="text-align:center;">作出行政处罚<br>决定机关名称</th>
            <th width="12%" style="text-align:center;">作出行政处罚<br>决定日期</th>
            <th width="12%" style="text-align:center;">公示日期</th>
            <th width="12%" style="text-align:center;">详情</th>

        </tr>
    </table>
    <div id="punDiv">
        <table cellspacing="0" cellpadding="0" class="detailsList" id="punTab">
    </table>
    </div>
    <br/>
</div>

<div id="chouchaxinxi" style="display:none;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="5" style="text-align:center;">抽查检查信息</th>
        </tr>
        <tr width="95%">
            <th width="5%" style="text-align:center;">序号</th>
            <th width="35%" style="text-align:center;">检查实施机关</th>
            <th width="10%" style="text-align:center;">类型</th>
            <th width="15%" style="text-align:center;">日期</th>
            <!--<th width="15%" style="text-align:center;">公示日期</th>-->
            <th width="25%" style="text-align:center;">结果</th>
        </tr>
     </table>
    <div id="spotCheckDiv">
    <table cellpadding="0" cellspacing="0" class="detailsList">
    </table>
    </div>

    <br/>
</div>

</div>
</div>
</div>
<br/> <br/>
<div class="banqun">
    版权所有：西藏自治区工商行政管理局 业务咨询电话：0891-6336063技术支持电话：0891-6335788<br/>
    地址：拉萨市城关区宇拓路28号 邮编：850000
</div>
</body>
</html>
<script>
var pageNo1 = 1;
var pageNo2 = 1;
var pageNo3 = 1;
var pageNo4 = 1;
var pageNo5 = 1;//行政处罚
var pageNo6 = 1;//经营异常
function goPage1(flag, n) {
    var request = new ajax.Request();
    pageNo1 = n;
    setRed(flag, n);
    if (flag != null && flag == 'mem') {
        request.loadTextByGet("/QueryMemList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshMemList);
    } else if (flag != null && flag == 'child') {
        request.loadTextByGet("/QueryChildList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshChildList);
    }else if (flag != null && flag == 'alt') {
        request.loadTextByGet("/QueryAltList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshAltList);
    } else {
        request.loadTextByGet("/QueryInvList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshInvList);
    }

}
function goPage2(flag, n) {
    var request = new ajax.Request();
    pageNo2 = n;
    setRed(flag, n);
    if (flag != null && flag == 'mem') {
        request.loadTextByGet("/QueryMemList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshMemList);
    } else if (flag != null && flag == 'child') {
        request.loadTextByGet("/QueryChildList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshChildList);
    }else if (flag != null && flag == 'alt') {
        request.loadTextByGet("/QueryAltList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshAltList);
    } else {
        request.loadTextByGet("/QueryInvList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshInvList);
    }

}
function goPage3(flag, n) {
    var request = new ajax.Request();
    pageNo3 = n;
    setRed(flag, n);
    if (flag != null && flag == 'mem') {
        request.loadTextByGet("/QueryMemList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshMemList);
    } else if (flag != null && flag == 'child') {
        request.loadTextByGet("/QueryChildList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshChildList);
    }else if (flag != null && flag == 'alt') {
        request.loadTextByGet("/QueryAltList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshAltList);
    }else if (flag != null && flag == 'serill') {
        request.loadTextByGet("/QuerySerillList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshSerillList);
    }else if (flag != null && flag == 'spotCheck') {
        request.loadTextByGet("/QuerySpotCheckList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshSpotCheckList);
    } else {
        request.loadTextByGet("/QueryInvList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshInvList);
    }

}
    function slipFive(flag,lastMaxPage,totalPage,preOrNext) {
        var tpage = '2';
        var CurrentFirstPage ;
        if(preOrNext=='next'){
            if(lastMaxPage>=totalPage){
                CurrentFirstPage = (Math.floor(totalPage/5))*5+1;
            }else{
                CurrentFirstPage = lastMaxPage + 1;
            }
        }else{
            if(lastMaxPage<=5){
                CurrentFirstPage = 1;
            }else{
                 if(lastMaxPage%5==0){
                    CurrentFirstPage = lastMaxPage - 9;
                }else{
                    CurrentFirstPage = (Math.floor(lastMaxPage/5))*5 - 4;
                }
            }
        }
       	if (flag != null && flag == 'inv') {
            tpage = '2';
        } else if (flag != null && flag == 'mem') {
            tpage = '1';
        } else if (flag != null && flag == 'child') {
            tpage = '0';
        } else if (flag != null && flag == 'alt') {
            tpage = '1';
        }else if (flag != null && flag == 'pledge') {
            tpage = '0';
        }else if (flag != null && flag == 'mort') {
            tpage = '0';
        }else if (flag != null && flag == 'exc') {
            tpage = '1';
        }else if (flag != null && flag == 'serill') {
            tpage = '0';
        }else if (flag != null && flag == 'puun') {
            tpage = '0';
        }else if (flag != null && flag == 'spotCheck') {
            tpage = '0';
        }

        goShowNextFive(flag, tpage,CurrentFirstPage,totalPage);
    }
    function goShowNextFive(flag, n,CurrentFirstPage,totalPage) {
        var currentMaxPage = 0;
        if((CurrentFirstPage+4)<totalPage){
            currentMaxPage = CurrentFirstPage+4;
        } else{
            currentMaxPage = totalPage;
        }
        var request = new ajax.Request();
        if (flag != null && flag == 'inv') {
            var invPagination = document.getElementById("invPagination");
            invPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"inv\","+currentMaxPage+",2,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"ainv"+i+"\" href='javascript:goPage3(\"inv\","+i+");'><span id=\"spaninv"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"inv\","+currentMaxPage+",2,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            invPagination.innerHTML= innerHTML;
            goPage3("inv",CurrentFirstPage);
        }else if (flag != null && flag == 'mem') {
            var memPagination = document.getElementById("memPagination");
            memPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"mem\","+currentMaxPage+",1,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"amem"+i+"\" href='javascript:goPage3(\"mem\","+i+");'><span id=\"spanmem"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"mem\","+currentMaxPage+",1,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            memPagination.innerHTML= innerHTML;
            goPage3("mem",CurrentFirstPage);
        } else if (flag != null && flag == 'child') {
            var childPagination = document.getElementById("childPagination");
            childPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"child\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"achild"+i+"\" href='javascript:goPage3(\"child\","+i+");'><span id=\"spanchild"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"child\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            childPagination.innerHTML= innerHTML;
            goPage3("child",CurrentFirstPage);
        }else if (flag != null && flag == 'alt') {
            var altPagination = document.getElementById("altPagination");
            altPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"alt\","+currentMaxPage+",1,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"aalt"+i+"\" href='javascript:goPage3(\"alt\","+i+");'><span id=\"spanalt"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"alt\","+currentMaxPage+",1,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            altPagination.innerHTML= innerHTML;
            goPage3("alt",CurrentFirstPage);
        }else if (flag != null && flag == 'pledge') {
            var pledgePagination = document.getElementById("pledgePagination");
            pledgePagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"pledge\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"apledge"+i+"\" href='javascript:goPage9(\"pledge\","+i+");'><span id=\"spanpledge"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"pledge\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            pledgePagination.innerHTML= innerHTML;
            goPage9("pledge",CurrentFirstPage);
        }else if (flag != null && flag == 'mort') {
            var mortPagination = document.getElementById("mortPagination");
            mortPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"mort\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"amort"+i+"\" href='javascript:goPage10(\"mort\","+i+");'><span id=\"spanmort"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"mort\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            mortPagination.innerHTML= innerHTML;
            goPage10("mort",CurrentFirstPage);
        }else if (flag != null && flag == 'exc') {
            var excPagination = document.getElementById("excPagination");
            excPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"exc\","+currentMaxPage+",1,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"aexc"+i+"\" href='javascript:goPage6(\"exc\","+i+");'><span id=\"spanexc"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"exc\","+currentMaxPage+",1,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            excPagination.innerHTML= innerHTML;
            goPage6("exc",CurrentFirstPage);
        }else if (flag != null && flag == 'serill') {
            var serillPagination = document.getElementById("serillPagination");
            serillPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"serill\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"aserill"+i+"\" href='javascript:goPage3(\"serill\","+i+");'><span id=\"spanserill"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"serill\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            serillPagination.innerHTML= innerHTML;
            goPage3("serill",CurrentFirstPage);
        }else if (flag != null && flag == 'pun') {
            var punPagination = document.getElementById("punPagination");
            punPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"pun\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"apun"+i+"\" href='javascript:goPage5(\"pun\","+i+");'><span id=\"spanpun"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"pun\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            punPagination.innerHTML= innerHTML;
            goPage5("pun",CurrentFirstPage);
        }else if (flag != null && flag == 'spotCheck') {
            var spotCheckPagination = document.getElementById("spotCheckPagination");
            spotCheckPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"spotCheck\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"aspotCheck"+i+"\" href='javascript:goPage3(\"spotCheck\","+i+");'><span id=\"spanspotCheck"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"spotCheck\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            spotCheckPagination.innerHTML= innerHTML;
            goPage3("spotCheck",CurrentFirstPage);
        }

    }
function goPage4(flag, n) {
    var request = new ajax.Request();
    pageNo4 = n;
    setRed(flag, n);
    if (flag != null && flag == 'mem') {
        request.loadTextByGet("/QueryMemList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshMemList);
    } else if (flag != null && flag == 'child') {
        request.loadTextByGet("/QueryChildList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshChildList);
    }else if (flag != null && flag == 'alt') {
        request.loadTextByGet("/QueryAltList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshAltList);
    } else {
        request.loadTextByGet("/QueryInvList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshInvList);
    }

}
function goPage5(flag, n) {
    var request = new ajax.Request();
    pageNo5 = n;
    setRed(flag, n);
    request.loadTextByGet("/QueryPunList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776&ran="+Math.random(), refreshPunList);
}

function goPage6(flag, n) {
    var request = new ajax.Request();
    pageNo6 = n;
    setRed(flag, n);
    request.loadTextByGet("/QueryExcList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776&ran="+Math.random(), refreshExcList);
}


function refreshInvList(message) {
    var divTab = document.getElementById("invDiv");
    divTab.innerHTML = '';
    divTab.innerHTML = message.substr(1, message.length - 2);
}
function refreshMemList(message) {
    var memDiv = document.getElementById("memDiv");
    memDiv.innerHTML = '';
    memDiv.innerHTML = message.substr(1, message.length - 2);
}
function refreshChildList(message) {
    var childDiv = document.getElementById("childDiv");
    childDiv.innerHTML = '';
    childDiv.innerHTML = message.substr(1, message.length - 2);
}
function refreshAltList(message) {
    var altDiv = document.getElementById("altDiv");
    altDiv.innerHTML = '';
    altDiv.innerHTML = message.substr(1, message.length - 2);
    doExpand();
}
function refreshPunList(message) {
    var punDiv = document.getElementById("punDiv");
    punDiv.innerHTML = '';
    punDiv.innerHTML = message.substr(1, message.length - 2);
    doExpand_pun();
}
function refreshExcList(message) {
    var excDiv = document.getElementById("excDiv");
    excDiv.innerHTML = '';
    excDiv.innerHTML = message.substr(1, message.length - 2);
    doExpand_exc();
}
    function refreshSerillList(message) {
        var serillDiv = document.getElementById("serillDiv");
        serillDiv.innerHTML = '';
        serillDiv.innerHTML = message.substr(1, message.length - 2);
    }
    function refreshSpotCheckList(message) {
        var spotCheckDiv = document.getElementById("spotCheckDiv");
        spotCheckDiv.innerHTML = '';
        spotCheckDiv.innerHTML = message.substr(1, message.length - 2);
    }

function next1(flag) {
    var tpage = '2';
    if (flag != null && flag == 'mem') {
        tpage = '1';
    } else if (flag != null && flag == 'child') {
        tpage = '0';
    } else if (flag != null && flag == 'alt') {
        tpage = '1';
    }

    goPage1(flag, tpage);
}
function next2(flag) {
    var tpage = '2';
    if (flag != null && flag == 'mem') {
        tpage = '1';
    } else if (flag != null && flag == 'child') {
        tpage = '0';
    } else if (flag != null && flag == 'alt') {
        tpage = '1';
    }

    goPage2(flag, tpage);
}
function next3(flag) {
    var tpage = '2';
    if (flag != null && flag == 'mem') {
        tpage = '1';
    } else if (flag != null && flag == 'child') {
        tpage = '0';
    } else if (flag != null && flag == 'alt') {
        tpage = '1';
    }else if (flag != null && flag == 'serill') {
        tpage = '0';
    }else if (flag != null && flag == 'spotCheck') {
        tpage = '0';
    }

    goPage3(flag, tpage);
}
function next4(flag) {
    var tpage = '2';
    if (flag != null && flag == 'mem') {
        tpage = '1';
    } else if (flag != null && flag == 'child') {
        tpage = '0';
    } else if (flag != null && flag == 'alt') {
        tpage = '1';
    }

    goPage4(flag, tpage);
}
function next5(flag) {
    var tpage = '0';
    goPage5(flag, tpage);
}
function next6(flag) {
    var tpage = '1';
    goPage6(flag, tpage);
}



function pre1(flag) {
    goPage1(flag, 1);
}
function pre2(flag) {
    goPage2(flag, 1);
}
function pre3(flag) {
    goPage3(flag, 1);
}
function pre4(flag) {
    goPage4(flag, 1);
}
function pre5(flag) {
    goPage5(flag, 1);
}
function pre6(flag) {
    goPage6(flag, 1);
}


    function setRed(flag, n) {
        var currentFirstPage = Math.ceil(n/5)*5-4;
        var tpage = '2';
        if (flag != null && flag == 'inv') {
            tpage = '2';
        }else if (flag != null && flag == 'mem') {
            tpage = '1';
        } else if (flag != null && flag == 'child') {
            tpage = '0';
        } else if (flag != null && flag == 'alt') {
            tpage = '1';
        }else if (flag != null && flag == 'pun') {
            tpage = '0';
        }else if (flag != null && flag == 'exc') {
            tpage = '1';
        }else if (flag != null && flag == 'pledge') {
            tpage = '0';
        } else if (flag != null && flag == 'mort') {
            tpage = '0';
        }else if (flag != null && flag == 'serill') {
            tpage = '0';
        } else if (flag != null && flag == 'spotCheck') {
            tpage = '0';
        }

        for (var i = currentFirstPage; i <= (currentFirstPage+4); i++) {
            if(i>tpage){

            }else{
                document.getElementById("span" + flag + i).style.color = "";
                document.getElementById("a" + flag + i).style.textDecoration = "underline";
            }
        }
        document.getElementById("span" + flag + n).style.color = "red";
        document.getElementById("a" + flag + n).style.textDecoration = "none";
    }

var pageNo9 = 1;//股权出质
function goPage9(flag, n) {
    var request = new ajax.Request();
    pageNo9 = n;
    setRed(flag, n);
    request.loadTextByGet("/QueryPledgeList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776&ran=" + Math.random(), refreshPledgeList);
}

function next9(flag) {
    var tpage = '0';
    goPage9(flag, tpage);
}

function pre9(flag) {
    goPage9(flag, 1);
}

function refreshPledgeList(message) {
    var pledgeDiv = document.getElementById("pledgeDiv");
    pledgeDiv.innerHTML = '';
    pledgeDiv.innerHTML = message.substr(1, message.length - 2);
}

var pageNo10 = 1;//动产抵押
function goPage10(flag, n) {
    var request = new ajax.Request();
    pageNo10 = n;
    setRed(flag, n);
    request.loadTextByGet("/QueryMortList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776&ran=" + Math.random(), refreshMortList);
}

function next10(flag) {
    var tpage = '0';
    goPage10(flag, tpage);
}

function pre10(flag) {
    goPage10(flag, 1);
}

function refreshMortList(message) {
    var mortDiv = document.getElementById("mortDiv");
    mortDiv.innerHTML = '';
    mortDiv.innerHTML = message.substr(1, message.length - 2);
}
 //显示更多
    function showAlterMore(rowIndex,size){
        var a = document.getElementById("a"+rowIndex);
        var td = document.getElementById("td"+rowIndex);
        var detailTd = document.getElementById("detailTd"+rowIndex);
        var div = document.getElementById("xingzhengchufa");
        var ele = document.getElementById("7");
        var showDiv1 = document.getElementById("tr"+rowIndex+1);
        if(showDiv1.style.display=="none"){
            a.innerText="收起更多";
            td.rowSpan=size+1;
            detailTd.rowSpan=size+1;
        }else{
             a.innerText="更多";
             td.rowSpan = 2;
             detailTd.rowSpan = 2;
             changeStyle('tabs',ele);
             if(div.style.display="block"){
                div.style.display="";
             }else{
                 div.style.display="block";
             }
        }

        for(var i=1;i<size;i++){
            var showDiv = document.getElementById("tr"+rowIndex+i);
            if(showDiv.style.display=="none"){
                   showDiv.style.display="";
                }else{
                   showDiv.style.display="none";
                }
        }

    }
/*经营异常展开、缩起*/
    var arr_excIn = new Array();
    var arr_excOut = new Array();
    /*展开内容*/
    doExpand_exc();
/*变更信息展开、缩起*/
    var arr_altBe = new Array();
    var arr_altAf = new Array();
    /*展开内容*/
    doExpand();

/*行政处罚 内容展开、收起*/
    var arr_punBasis = new Array();
    var arr_punResult = new Array();
    var arr_punAlt = new Array();

</script>'''

enterprise_html_gdxx_beijing = '''





<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet" />
	<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script><!-- 1.9版本jQuery js   -->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/pubInfo.js"></script><!-- 北京首页pubInfo.js js   -->
</head>

<body>
<div id="header"  style="height:119px;"><img src="/country_credit/bj/images/header_bj.jpg" width="990"/></div>
<br/>
	<div id="details" class="clear">
	<h2  style="background-color:#ce010c ;color:white;">北京中关村科技投资有限公司 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h2><!-- 注册号： -->
	<form action="gjjbj/gjjQueryCreditAction!touzirenInfo.dhtml" method="post"  name="iframeFrame" id="iframeFrame">
	<input type="hidden" id="pageNos" name="pageNos" value="1" />
	<input type="hidden" id="inv" name="chr_id" value="F8EEBE0AF72F4FB5BE8B9D9111B94F1E"/>
	   <div id="sifapanding" >
	<br>
	<table  cellpadding="0" cellspacing="0" class="detailsList">
		<tr><th colspan="9" style="text-align:center;">股东及出资信息 </th></tr>
        <tr width="95%">
		  <th width="10%" style="text-align:center;" rowspan="2">股东</th>
          <th width="13%" style="text-align:center;" rowspan="2">认缴额（万元）</th>
          <th width="13%" style="text-align:center;" rowspan="2">实缴额（万元）</th>
		  <th width="32%" style="text-align:center;" colspan="3">认缴明细</th>
          <th width="32%" style="text-align:center;" colspan="3">实缴明细</th>
        </tr>
         <tr width="95%">
		  <th width="10%" style="text-align:center;">认缴出资方式</th>
          <th width="10%" style="text-align:center;">认缴出资额（万元）</th>
          <th width="12%" style="text-align:center;">认缴出资日期</th>
		  <th width="10%" style="text-align:center;">实缴出资方式</th>
          <th width="10%" style="text-align:center;">实缴出资额（万元）</th>
		  <th width="12%" style="text-align:center;">实缴出资日期</th>
        </tr>

         	<tr>
			  <td style="text-align:left;"  >中融嘉尚（北京）投资管理有限公司</td>
	          <td style="text-align:right;" >2000</td>
	          <td style="text-align:right;">2000</td>
			  <td style="text-align:left;"></td>
	          <td style="text-align:right;">2000</td>
	          <td style="text-align:center;"></td>
	          <td style="text-align:left;"></td>
	          <td style="text-align:right;">2000</td>
			  <td style="text-align:center;"></td>
	        </tr>



			<tr><th colspan='9' style='text-align:right;'></th></tr>


	</table>
	</form></div>
<div id="footer"><img src="/country_credit/bj/images/footer_beijing1.jpg" width="990"/></div>
</body>
</html>'''

enterprise_html_gdxx_xizang = '''

 <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>全国企业信用信息公示系统</title>
<link href="/css/public3.css" type="text/css" rel="stylesheet" />
	<script type="text/javascript">
		function closephone(){
			document.getElementById('sxphone').style.display='none';
			document.getElementById('bgDiv').style.display='none';
		}
		function iframeLoad(){
			var sxphoneHeight=$('#sxphone').height();
			$('#phoneiframe').height(sxphoneHeight-40);
		}
		function openphone(){
			window.scrollTo(0,0);
				var winWidth = 0;
		        var winHeight = 0;
		        if (window.innerWidth)
		              winWidth = window.innerWidth;
		        else if ((document.body) && (document.body.clientWidth))
		              winWidth = document.body.clientWidth;
		        //获取窗口高度
		        if (window.innerHeight)
		              winHeight = window.innerHeight;
		        else if ((document.body) && (document.body.clientHeight))
		              winHeight = document.body.clientHeight;

			var sxphone=document.getElementById("sxphone");
			if(sxphone){
				sxphone.top="50%";
				sxphone.left="50%";
				 //获取窗口宽度
				sxphone.style.display="";
				document.getElementById('bgDiv').style.display='';
			}
			else{
			 	var bgObj =document.createElement("div");
			    bgObj.setAttribute('id','bgDiv');
			    bgObj.style.position="absolute";
			    bgObj.style.top="0";
			    bgObj.style.background="#777";
			    bgObj.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75";
			    bgObj.style.opacity="0.6";
			    bgObj.style.left="0";
			    bgObj.style.width=winWidth + "px";
			    bgObj.style.height=winHeight + "px";
			    bgObj.style.zIndex = "1000";
			    bgObj.style.MozOpacity="0.7";

			    document.body.appendChild(bgObj);
				var div = document.createElement("div");
				//div.id="sxphone";
				div.setAttribute('id','sxphone');
				div.style.height="80%";
				div.style.width="800px";
				div.style.border="0px solid red";
				div.style.position="absolute";
				div.style.left="50%";
				div.style.margin="0 0 0 -400px";
				div.style.top="5%";
				div.style.zIndex = "10001";
				div.style.MozBorderRadius="5px";
				div.style.webkitBorderRadius="5px";
				div.style.borderRadius="5px";
				div.style.background="#2D84B2";
				div.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=100,finishOpacity=100";
				div.style.padding="0";
				  div.style.MozOpacity="1";
				div.innerHTML = "<div style='font-weight: bold;color: #fff;height:20px;padding:5px 20px;font-size:14px'><img src='/js/skins/ZCMS/images/icon.gif'/>咨询电话<span style='float:right;'>"+
				"<a style='color:#fff;font-size:12px' href='javascript:closephone();' title='关闭'>关闭</a></span></div>"+
					"<iframe id='phoneiframe' src='/sxphone.jspx' style='width:790px;border:0px solid red;padding:0;margin:5px 5px -10px 5px;' onload='iframeLoad()'></iframe>";
				document.body.appendChild(div);
				var ua = navigator.userAgent;
			    if (ua.lastIndexOf("MSIE 6.0") != -1) {
			    	var phoneiframe=document.getElementById("phoneiframe");
			    	//phoneiframe.style.width="840px";
			    	phoneiframe.style.height="580px";
			    	phoneiframe.style.marginRight="-15px";
				}
			}
		}
		function iframeLoadHb(){
			var sxphoneHeight=$('#sxphone').height();
			$('#phoneiframe').height(sxphoneHeight-60);
		}
			function openphonehb(){
			window.scrollTo(0,0);
				var winWidth = 0;
		        var winHeight = 0;
		        if (window.innerWidth)
		              winWidth = window.innerWidth;
		        else if ((document.body) && (document.body.clientWidth))
		              winWidth = document.body.clientWidth;
		        //获取窗口高度
		        if (window.innerHeight)
		              winHeight = window.innerHeight;
		        else if ((document.body) && (document.body.clientHeight))
		              winHeight = document.body.clientHeight;

			var sxphone=document.getElementById("sxphone");
			if(sxphone){
				sxphone.top="50%";
				sxphone.left="50%";
				 //获取窗口宽度
				sxphone.style.display="";
				document.getElementById('bgDiv').style.display='';
			}
			else{
			 	var bgObj =document.createElement("div");
			    bgObj.setAttribute('id','bgDiv');
			    bgObj.style.position="absolute";
			    bgObj.style.top="0";
			    bgObj.style.background="#777";
			    bgObj.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75";
			    bgObj.style.opacity="0.6";
			    bgObj.style.left="0";
			    bgObj.style.width=winWidth + "px";
			    bgObj.style.height=winHeight + "px";
			    bgObj.style.zIndex = "1000";
			    bgObj.style.MozOpacity="0.7";

			    document.body.appendChild(bgObj);
				var div = document.createElement("div");
				//div.id="sxphone";
				div.setAttribute('id','sxphone');
				div.style.height="80%";
				div.style.width="800px";
				div.style.border="0px solid red";
				div.style.position="absolute";
				div.style.left="50%";
				div.style.margin="0 0 0 -400px";
				div.style.top="5%";
				div.style.zIndex = "10001";
				div.style.background="#ECEEEE";
				div.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=100,finishOpacity=100";
				div.style.padding="0";
				  div.style.MozOpacity="1";
				div.innerHTML = "<div style='font-weight: bold;color: #000;height:20px;padding:5px 20px;font-size:14px;'>咨询电话<span style='float:right;'>"+
				"<a style='color:#000;font-size:12px' href='javascript:closephone();' title='关闭'>关闭</a></span></div>"+
				"<hr />"+
					"<iframe id='phoneiframe' src='/hbphone.jspx' style='width:790px;border:0px solid red;padding:0;margin:5px 5px -10px 5px;' onload='iframeLoadHb()'></iframe>";
				document.body.appendChild(div);
				var ua = navigator.userAgent;
			    if (ua.lastIndexOf("MSIE 6.0") != -1) {
			    	var phoneiframe=document.getElementById("phoneiframe");
			    	//phoneiframe.style.width="840px";
			    	phoneiframe.style.height="580px";
			    	phoneiframe.style.marginRight="-15px";
				}
			}
		}
	</script>
</head>
<style type="text/css">
  .top{width:990px; height:124px; background:url("/images/xizang.png") no-repeat; }
  .banqun{width:990px; height:59px; bottom:0; background:url("/images/ban-bj.png") repeat-x  ; padding-top:20px;font-size:14px; text-align:center; margin:0 auto;color:#fff;font-family:"微软雅黑";}
</style>
<body>
<div id="header"><img src="/images/xizang.png" width="990" /></div><br/><br/><br/><br/>
<div id="details" class="clear">

        <h2 >
            西藏城市发展投资股份有限公司 &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp; 注册号/统一社会信用代码：540000100003419&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
            &nbsp;&nbsp;&nbsp;
        </h2>
     <br/>
    <br/>
     <table  cellpadding="0" cellspacing="0" class="detailsList" >
            <tr><th colspan="9" style="text-align:center;">股东（发起人）及出资信息 </th></tr>
            <tr width="95%">
              <th width="10%" style="text-align:center;" rowspan="2">股东（发起人）</th>
              <th width="12%" style="text-align:center;" rowspan="2">认缴额（万元）</th>
              <th width="12%" style="text-align:center;" rowspan="2">实缴额（万元）</th>
              <th width="33%" style="text-align:center;" colspan="3">认缴明细</th>
              <th width="33%" style="text-align:center;" colspan="3">实缴明细</th>
            </tr>
            <tr>
              <th width="10%" style="text-align:center;">认缴出资方式</th>
              <th width="10%" style="text-align:center;">认缴出资额（万元）</th>
              <th width="13%" style="text-align:center;">认缴出资日期</th>

              <th width="10%" style="text-align:center;">实缴出资方式</th>
              <th width="10%" style="text-align:center;">实缴出资额（万元）</th>
              <th width="13%" style="text-align:center;">实缴出资日期</th>
            </tr>
				<tr>
				  <td rowspan="1">社会公众股</td>
				  <td rowspan="1">15351</td>
                  <td rowspan="1"></td>
                          <td rowspan="0">货币</td>
                          <td rowspan="0">15351万人民币元</td>
                          <td rowspan="0">2014年10月31日</td>
<td></td><td></td><td></td>
                </tr>
				</table>
	</div>
<br/> <br/>
<div class="banqun">
    版权所有：西藏自治区工商行政管理局 业务咨询电话：0891-6336063技术支持电话：0891-6335788<br/>
    地址：拉萨市城关区宇拓路28号 邮编：850000
</div>
</div>
</body>
</html>'''

enterprise_html_xizang_zyry_and_other='''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <META HTTP-EQUIV="pragma" CONTENT="no-cache"/>
    <META HTTP-EQUIV="Cache-Control" CONTENT="no-cache, must-revalidate"/>
    <META HTTP-EQUIV="expires" CONTENT="Wed, 26 Feb 1997 08:21:57 GMT"/>
    <title>全国企业信用信息公示系统</title>
    <link href="/css/public3.css" type="text/css" rel="stylesheet"/>
    <script type="text/javascript" src="/js/ajax.js"></script>
    <script type="text/javascript" src="/js/infoExpand.js"></script>
	<script type="text/javascript">
		function closephone(){
			document.getElementById('sxphone').style.display='none';
			document.getElementById('bgDiv').style.display='none';
		}
		function iframeLoad(){
			var sxphoneHeight=$('#sxphone').height();
			$('#phoneiframe').height(sxphoneHeight-40);
		}
		function openphone(){
			window.scrollTo(0,0);
				var winWidth = 0;
		        var winHeight = 0;
		        if (window.innerWidth)
		              winWidth = window.innerWidth;
		        else if ((document.body) && (document.body.clientWidth))
		              winWidth = document.body.clientWidth;
		        //获取窗口高度
		        if (window.innerHeight)
		              winHeight = window.innerHeight;
		        else if ((document.body) && (document.body.clientHeight))
		              winHeight = document.body.clientHeight;

			var sxphone=document.getElementById("sxphone");
			if(sxphone){
				sxphone.top="50%";
				sxphone.left="50%";
				 //获取窗口宽度
				sxphone.style.display="";
				document.getElementById('bgDiv').style.display='';
			}
			else{
			 	var bgObj =document.createElement("div");
			    bgObj.setAttribute('id','bgDiv');
			    bgObj.style.position="absolute";
			    bgObj.style.top="0";
			    bgObj.style.background="#777";
			    bgObj.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75";
			    bgObj.style.opacity="0.6";
			    bgObj.style.left="0";
			    bgObj.style.width=winWidth + "px";
			    bgObj.style.height=winHeight + "px";
			    bgObj.style.zIndex = "1000";
			    bgObj.style.MozOpacity="0.7";

			    document.body.appendChild(bgObj);
				var div = document.createElement("div");
				//div.id="sxphone";
				div.setAttribute('id','sxphone');
				div.style.height="80%";
				div.style.width="800px";
				div.style.border="0px solid red";
				div.style.position="absolute";
				div.style.left="50%";
				div.style.margin="0 0 0 -400px";
				div.style.top="5%";
				div.style.zIndex = "10001";
				div.style.MozBorderRadius="5px";
				div.style.webkitBorderRadius="5px";
				div.style.borderRadius="5px";
				div.style.background="#2D84B2";
				div.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=100,finishOpacity=100";
				div.style.padding="0";
				  div.style.MozOpacity="1";
				div.innerHTML = "<div style='font-weight: bold;color: #fff;height:20px;padding:5px 20px;font-size:14px'><img src='/js/skins/ZCMS/images/icon.gif'/>咨询电话<span style='float:right;'>"+
				"<a style='color:#fff;font-size:12px' href='javascript:closephone();' title='关闭'>关闭</a></span></div>"+
					"<iframe id='phoneiframe' src='/sxphone.jspx' style='width:790px;border:0px solid red;padding:0;margin:5px 5px -10px 5px;' onload='iframeLoad()'></iframe>";
				document.body.appendChild(div);
				var ua = navigator.userAgent;
			    if (ua.lastIndexOf("MSIE 6.0") != -1) {
			    	var phoneiframe=document.getElementById("phoneiframe");
			    	//phoneiframe.style.width="840px";
			    	phoneiframe.style.height="580px";
			    	phoneiframe.style.marginRight="-15px";
				}
			}
		}
		function iframeLoadHb(){
			var sxphoneHeight=$('#sxphone').height();
			$('#phoneiframe').height(sxphoneHeight-60);
		}
			function openphonehb(){
			window.scrollTo(0,0);
				var winWidth = 0;
		        var winHeight = 0;
		        if (window.innerWidth)
		              winWidth = window.innerWidth;
		        else if ((document.body) && (document.body.clientWidth))
		              winWidth = document.body.clientWidth;
		        //获取窗口高度
		        if (window.innerHeight)
		              winHeight = window.innerHeight;
		        else if ((document.body) && (document.body.clientHeight))
		              winHeight = document.body.clientHeight;

			var sxphone=document.getElementById("sxphone");
			if(sxphone){
				sxphone.top="50%";
				sxphone.left="50%";
				 //获取窗口宽度
				sxphone.style.display="";
				document.getElementById('bgDiv').style.display='';
			}
			else{
			 	var bgObj =document.createElement("div");
			    bgObj.setAttribute('id','bgDiv');
			    bgObj.style.position="absolute";
			    bgObj.style.top="0";
			    bgObj.style.background="#777";
			    bgObj.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75";
			    bgObj.style.opacity="0.6";
			    bgObj.style.left="0";
			    bgObj.style.width=winWidth + "px";
			    bgObj.style.height=winHeight + "px";
			    bgObj.style.zIndex = "1000";
			    bgObj.style.MozOpacity="0.7";

			    document.body.appendChild(bgObj);
				var div = document.createElement("div");
				//div.id="sxphone";
				div.setAttribute('id','sxphone');
				div.style.height="80%";
				div.style.width="800px";
				div.style.border="0px solid red";
				div.style.position="absolute";
				div.style.left="50%";
				div.style.margin="0 0 0 -400px";
				div.style.top="5%";
				div.style.zIndex = "10001";
				div.style.background="#ECEEEE";
				div.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=100,finishOpacity=100";
				div.style.padding="0";
				  div.style.MozOpacity="1";
				div.innerHTML = "<div style='font-weight: bold;color: #000;height:20px;padding:5px 20px;font-size:14px;'>咨询电话<span style='float:right;'>"+
				"<a style='color:#000;font-size:12px' href='javascript:closephone();' title='关闭'>关闭</a></span></div>"+
				"<hr />"+
					"<iframe id='phoneiframe' src='/hbphone.jspx' style='width:790px;border:0px solid red;padding:0;margin:5px 5px -10px 5px;' onload='iframeLoadHb()'></iframe>";
				document.body.appendChild(div);
				var ua = navigator.userAgent;
			    if (ua.lastIndexOf("MSIE 6.0") != -1) {
			    	var phoneiframe=document.getElementById("phoneiframe");
			    	//phoneiframe.style.width="840px";
			    	phoneiframe.style.height="580px";
			    	phoneiframe.style.marginRight="-15px";
				}
			}
		}
	</script>
    <script type="text/javascript">
        function r1() {
            document.getElementById('jibenxinxi').style.display = 'block';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';

        }
        function r2() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'block';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';

        }
        function r3() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'block';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';

        }
        function r4() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'block';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';
        }
        function r5() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'block';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';
        }
        function r6() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'block';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'none';
        }
        function r7() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'block';
            document.getElementById('chouchaxinxi').style.display = 'none';
        }
        function r8() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('guquanchuzhi').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('jingyingyichangminglu').style.display = 'none';
            document.getElementById('yanzhongweifaqiye').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('chouchaxinxi').style.display = 'block';
        }

        function togo(str) {
            if (str == '1') {
                window.location = '/businessPublicity.jspx?id=C0E2ED0898EBC82FD7567EC589AC9776';
            } else if (str == '2') {
                window.location = '/enterprisePublicity.jspx?id=C0E2ED0898EBC82FD7567EC589AC9776';
            }else if (str == '3') {
                window.location = '/otherDepartment.jspx?id=C0E2ED0898EBC82FD7567EC589AC9776';
            }else if(str == '4'){
                window.location = '/justiceAssistance.jspx?id=C0E2ED0898EBC82FD7567EC589AC9776';
            }
        }
          function changeTab() {
                var sourType = "";
                   if (sourType == "1") {
                    r5();
                    var tab = document.getElementById("5");
                    changeStyle('tabs',tab);
                  } else if (sourType == "2") {
                    r6();
                    var tab = document.getElementById("6");
                    changeStyle('tabs',tab);
                  } else if (sourType == "3") {
                    r8();
                    var tab = document.getElementById("8");
                    changeStyle('tabs',tab);
                  }
        }
        window.onload = function() {
              changeTab();
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

                }
                else {
                    liAry[i].className = "";
                }
            }
        }

        function ShowSpan(obj, n) {
            var span = obj.parentNode.getElementsByTagName("tabs");
            for (var i = 0; i < span.length; i++) {
                span[i].className = "current";
            }
            span[n].className = "";
            var li = obj.parentNode.getElementsByTagName("li")
            li[n].className = "current";
            for (var i = 0; i < li.length; i++) {
                if (i != n) {
                    li[i].className = "";
                }
                li[i].onmouseout = function () {
                    this.className = "current";
                }
            }
        }
    </script>

</head>
<style type="text/css">
    th,td{word-break:break-all;}
  .top{width:990px; height:124px; background:url("/images/xizang.png") no-repeat; }
  .banqun{width:990px; height:59px; bottom:0; background:url("/images/ban-bj.png") repeat-x  ; padding-top:20px;font-size:14px; text-align:center; margin:0 auto;color:#fff;font-family:"微软雅黑";clear:both;}
</style>

<body>
<div id="header">
    <div class="top">
        <div class="top-a">
		<a href="http://gsxt.saic.gov.cn"  style="font-size:14px ; font-family:'微软雅黑'">全国首页</a>&nbsp;&nbsp;<a href="/search.jspx"
		style="font-size:14px ; font-family:'微软雅黑'">地方局首页</a>
        </div>
    </div>
</div>
<br><br><br><br>

<div id="details" class="clear" style="min-height: 880px;height: auto;">

    <h2 >
         西藏城市发展投资股份有限公司 &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp; 注册号/统一社会信用代码：540000100003419&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;
    </h2>

<br/>

<div id="leftTabs">
    <ul>
        <li class="current" style="margin-bottom:2px;"><p>工<br/>商<br/>公<br/>示<br/>信<br/>息</p></li>
        <li onclick="togo('2')" style="margin-bottom:2px;"><p>企<br/>业<br/>公<br/>示<br/>信<br/>息</p></li>
        <li onclick="togo('3')" style="margin-bottom:2px;"><p>其<br/>他<br/>部<br/>门<br/>公<br/>示<br/>信<br/>息</p></li>
        <li onclick="togo('4')"  style="margin-bottom:2px;"><p>司<br/>法<br/>协<br/>助<br/>公<br/>示<br/>信<br/>息</p></li>
    </ul>
</div>
<div id="detailsCon" style="height:1038px;overflow:atuo">
<div class="dConBox">
<div class="tabs" id="tabs">
    <ul>
        <li id="1" class="current" onclick="r1(),changeStyle('tabs',this)">登记信息</li>
        <li id="2" onclick="r2(),changeStyle('tabs',this)">备案信息</li>
        <li id="4" onclick="r4(),changeStyle('tabs',this)">动产抵押登记信息</li>
        <li id="3" onclick="r3(),changeStyle('tabs',this)">股权出质登记信息</li>
        <li id="7" onclick="r7(),changeStyle('tabs',this)">行政处罚信息</li>
        <li id="5" onclick="r5(),changeStyle('tabs',this)">经营异常信息</li>
        <li id="6" onclick="r6(),changeStyle('tabs',this)">严重违法信息</li>
        <li id="8" onclick="r8(),changeStyle('tabs',this)">抽查检查信息</li>
    </ul>
</div>


<div id="beian" style="align:center;display:none;height: 850px;width:930px;overflow: auto">
    <br>
    <table style="width:100%;" id="t30" cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="939px">
            <th colspan="6" style="text-align:center;">主要人员信息</th>
        </tr>
        <th style="width:10%;text-align:center">序号</th>
        <th style="width:20%;text-align:center">姓名</th>
        <th style="width:20%;text-align:center">职务</th>
        <th style="width:10%;text-align:center">序号</th>
        <th style="width:20%;text-align:center">姓名</th>
        <th style="width:20%;text-align:center">职务</th>
        </tr>
    </table>
    <div id="memDiv">
        <table cellspacing="0" cellpadding="0" class="detailsList">
                        <tr>
                    <td style="width:10%;text-align:center">1</td>
                    <td style="width:20%">朱贤麟                        </td>
                    <td style="width:20%">董事长</td>

                    <td style="width:10%;text-align:center">2</td>
                    <td style="width:20%">陈卫东                        </td>
                    <td style="width:20%">董事</td>
                        </tr>

                        <tr>
                    <td style="width:10%;text-align:center">3</td>
                    <td style="width:20%">吴素芬                        </td>
                    <td style="width:20%">监事</td>

                    <td style="width:10%;text-align:center">4</td>
                    <td style="width:20%">颜学海                        </td>
                    <td style="width:20%">董事</td>
                        </tr>

                        <tr>
                    <td style="width:10%;text-align:center">5</td>
                    <td style="width:20%">董惠良                        </td>
                    <td style="width:20%">董事</td>

                    <td style="width:10%;text-align:center">6</td>
                    <td style="width:20%">王列新                        </td>
                    <td style="width:20%">监事</td>
                        </tr>

                        <tr>
                    <td style="width:10%;text-align:center">7</td>
                    <td style="width:20%">唐泽平                        </td>
                    <td style="width:20%">董事</td>

                    <td style="width:10%;text-align:center">8</td>
                    <td style="width:20%">曾云                          </td>
                    <td style="width:20%">董事</td>
                        </tr>

                        <tr>
                    <td style="width:10%;text-align:center">9</td>
                    <td style="width:20%">华伟                          </td>
                    <td style="width:20%">董事</td>

                    <td style="width:10%"></td><td style="width:20%"></td><td style="width:20%"></td></tr>
        </table>
    </div>
            <table cellpadding="0" cellspacing="0" class="detailsList">
                <th colspan="4" style="text-align:right;">
                    <span style="color:blue"><<</span>
                        &nbsp;<a id="amem1" href='javascript:goPage3("mem",1);' style="text-decoration:none"><span id="spanmem1" style="color:red">1</span></a>
                                                        &nbsp;<span style="color:blue">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
            </table>

    </br>

    <br>

    <table id="t31" cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="939px">
            <th colspan="4" style="text-align:center;">分支机构信息</th>
        </tr>
        <tr>
            <th style="text-align:center;width:10%;">序号</th>
            <th style="text-align:center;width:25%">注册号/统一社会信用代码</th>
            <th style="text-align:center;width:25%">名称</th>
            <th style="text-align:center;width:20%">登记机关</th>
        </tr>
    </table>
    <div id="childDiv">
        <table cellspacing="0" cellpadding="0" class="detailsList">
        </table>
    </div>

    <br>


    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="939px">
            <th colspan="5" style="text-align:center;">清算信息</th>
        </tr>
        <tr>
            <th style="width:20%">清算组负责人</th>
            <td colspan="4">


            </td>
        </tr>
        <tr>
            <th rowspan="">清算组成员 </th>
            <td colspan="4">
            </td>
        </tr>
    </table>
</div>

<div id="guquanchuzhi" style="display:none;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="11" style="text-align:center;">股权出质登记信息</th>
        </tr>
        <tr width="95%">
            <th width="5%" style="text-align:center;">序号</th>
            <th width="8%" style="text-align:center;">登记编号</th>
            <th width="6%" style="text-align:center;">出质人</th>
            <th width="13%" style="text-align:center;">证照/证件号码</th>
            <th width="8%" style="text-align:center;">出质股权数额</th>
            <th width="8%" style="text-align:center;">质权人</th>
            <th width="13%" style="text-align:center;">证照/证件号码</th>
            <th width="12%" style="text-align:center;">股权出质设立登记日期</th>
            <th width="7%" style="text-align:center;">状态</th>
            <th width="11%" style="text-align:center">公示日期</th>
            <th width="6%" style="text-align:center;">变化情况</th>
        </tr>
    </table>

    <div id="pledgeDiv">
        <table cellpadding="0" cellspacing="0" class="detailsList">
        </table>
    </div>

    <br/>
</div>

<div id="dongchandiya" style="display:none ;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="9" style="text-align:center;">动产抵押登记信息</th>
        </tr>
        <tr width="95%">
            <th width="5%" style="text-align:center;">序号</th>
            <th width="20%" style="text-align:center;">登记编号</th>
            <th width="12%" style="text-align:center;">登记日期</th>
            <th width="20%" style="text-align:center;">登记机关</th>
            <th width="15%" style="text-align:center;">被担保债权数额</th>
            <th width="7%" style="text-align:center;">状态</th>
            <th width="13%" style="text-align:center;">公示日期</th>
            <th width="10%" style="text-align:center;">详情</th>
        </tr>
    </table>

    <div id="mortDiv">
        <table cellpadding="0" cellspacing="0" class="detailsList">
    </table>
    </div>
    <br/>
</div>

<div id="jingyingyichangminglu" style="display:none;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="6" style="text-align:center;">经营异常信息</th>
        </tr>
        <tr width="95%">
            <th width="5%" style="text-align:center;">序号</th>
            <th width="20%" style="text-align:center;">列入经营异常名录原因</th>
            <th width="13%" style="text-align:center;">列入日期</th>
            <th width="25%" style="text-align:center;">移出经营异常名录原因</th>
            <th width="13%" style="text-align:center;">移出日期</th>
            <!--<th width="13%" style="text-align:center;">公示日期</th>-->
            <th width="19%" style="text-align:center;">作出决定机关</th>
        </tr>
    </table>
    <div id="excDiv">
        <table cellspacing="0" cellpadding="0" class="detailsList" id="excTab">
                <tr>
                   <td width="5%" style="text-align:center;">1</td>
                    <td width="20%">未在工商行政管理部门依照《企业信息公示暂行条例》第十条规定责令的期限内公示有关企业信息的</td>
                    <td width="13%" style="text-align:center">
                        2015年4月7日
                    </td>
                    <td width="25%">列入经营异常名录3年内且依照《经营异常名录管理办法》第七条规定被列入经营异常名录的企业履行公示义务后，申请移出</td>
                    <td width="13%" style="text-align:center">
                        2015年7月16日
                    </td>
                    <!--<td width="13%" style="text-align:center">-->
                           <!---->
                        <!--</td>-->
                    <td width="19%">西藏自治区工商行政管理局</td>
                </tr>

    </table>
    </div>
            <table cellpadding="0" cellspacing="0" class="detailsList">
                <th colspan="4" style="text-align:right;">
                    <span style="color:blue"><<</span>
                        &nbsp;<a id="aexc1" href='javascript:goPage6("exc",1);' style="text-decoration:none"><span id="spanexc1" style="color:red">1</span></a>
                                                        &nbsp;<span style="color:blue">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
            </table>

    <br/>
</div>

<div id="yanzhongweifaqiye" style="display:none;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="6" style="text-align:center;">严重违法信息</th>
        </tr>
        <tr width="95%">
            <th width="5%" style="text-align:center;">序号</th>
            <th width="15%" style="text-align:center;">列入严重违法企业名单原因</th>
            <th width="13%" style="text-align:center;">列入日期</th>
            <th width="20%" style="text-align:center;">移出严重违法企业名单原因</th>
            <th width="13%" style="text-align:center;">移出日期</th>
            <!--<th width="13%" style="text-align:center;">公示日期</th>-->
            <th width="23%" style="text-align:center;">作出决定机关</th>
        </tr>
    </table>
    <div id="serillDiv">
    <table cellpadding="0" cellspacing="0" class="detailsList">
     </table>
     </div>
    <br/>
</div>

<div id="xingzhengchufa" style="display:none;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="9" style="text-align:center;">行政处罚信息</th>
        </tr>
        <tr width="95%">
            <th width="5%"  style="text-align:center;">序号</th>
            <th width="10%" style="text-align:center;">行政处罚<br>决定书文号</th>
            <th width="20%" style="text-align:center;">违法行为类型</th>
            <th width="18%" style="text-align:center;">行政处罚内容</th>
            <th width="18%" style="text-align:center;">作出行政处罚<br>决定机关名称</th>
            <th width="12%" style="text-align:center;">作出行政处罚<br>决定日期</th>
            <th width="12%" style="text-align:center;">公示日期</th>
            <th width="12%" style="text-align:center;">详情</th>

        </tr>
    </table>
    <div id="punDiv">
        <table cellspacing="0" cellpadding="0" class="detailsList" id="punTab">
    </table>
    </div>
    <br/>
</div>

<div id="chouchaxinxi" style="display:none;height: 850px;width:930px;overflow: auto">
    <br/>
    <table cellpadding="0" cellspacing="0" class="detailsList">
        <tr width="95%">
            <th colspan="5" style="text-align:center;">抽查检查信息</th>
        </tr>
        <tr width="95%">
            <th width="5%" style="text-align:center;">序号</th>
            <th width="35%" style="text-align:center;">检查实施机关</th>
            <th width="10%" style="text-align:center;">类型</th>
            <th width="15%" style="text-align:center;">日期</th>
            <!--<th width="15%" style="text-align:center;">公示日期</th>-->
            <th width="25%" style="text-align:center;">结果</th>
        </tr>
     </table>
    <div id="spotCheckDiv">
    <table cellpadding="0" cellspacing="0" class="detailsList">
    </table>
    </div>

    <br/>
</div>

</div>
</div>
</div>
<br/> <br/>
<div class="banqun">
    版权所有：西藏自治区工商行政管理局 业务咨询电话：0891-6336063技术支持电话：0891-6335788<br/>
    地址：拉萨市城关区宇拓路28号 邮编：850000
</div>
</body>
</html>
<script>
var pageNo1 = 1;
var pageNo2 = 1;
var pageNo3 = 1;
var pageNo4 = 1;
var pageNo5 = 1;//行政处罚
var pageNo6 = 1;//经营异常
function goPage1(flag, n) {
    var request = new ajax.Request();
    pageNo1 = n;
    setRed(flag, n);
    if (flag != null && flag == 'mem') {
        request.loadTextByGet("/QueryMemList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshMemList);
    } else if (flag != null && flag == 'child') {
        request.loadTextByGet("/QueryChildList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshChildList);
    }else if (flag != null && flag == 'alt') {
        request.loadTextByGet("/QueryAltList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshAltList);
    } else {
        request.loadTextByGet("/QueryInvList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshInvList);
    }

}
function goPage2(flag, n) {
    var request = new ajax.Request();
    pageNo2 = n;
    setRed(flag, n);
    if (flag != null && flag == 'mem') {
        request.loadTextByGet("/QueryMemList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshMemList);
    } else if (flag != null && flag == 'child') {
        request.loadTextByGet("/QueryChildList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshChildList);
    }else if (flag != null && flag == 'alt') {
        request.loadTextByGet("/QueryAltList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshAltList);
    } else {
        request.loadTextByGet("/QueryInvList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshInvList);
    }

}
function goPage3(flag, n) {
    var request = new ajax.Request();
    pageNo3 = n;
    setRed(flag, n);
    if (flag != null && flag == 'mem') {
        request.loadTextByGet("/QueryMemList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshMemList);
    } else if (flag != null && flag == 'child') {
        request.loadTextByGet("/QueryChildList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshChildList);
    }else if (flag != null && flag == 'alt') {
        request.loadTextByGet("/QueryAltList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshAltList);
    }else if (flag != null && flag == 'serill') {
        request.loadTextByGet("/QuerySerillList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshSerillList);
    }else if (flag != null && flag == 'spotCheck') {
        request.loadTextByGet("/QuerySpotCheckList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshSpotCheckList);
    } else {
        request.loadTextByGet("/QueryInvList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshInvList);
    }

}
    function slipFive(flag,lastMaxPage,totalPage,preOrNext) {
        var tpage = '2';
        var CurrentFirstPage ;
        if(preOrNext=='next'){
            if(lastMaxPage>=totalPage){
                CurrentFirstPage = (Math.floor(totalPage/5))*5+1;
            }else{
                CurrentFirstPage = lastMaxPage + 1;
            }
        }else{
            if(lastMaxPage<=5){
                CurrentFirstPage = 1;
            }else{
                 if(lastMaxPage%5==0){
                    CurrentFirstPage = lastMaxPage - 9;
                }else{
                    CurrentFirstPage = (Math.floor(lastMaxPage/5))*5 - 4;
                }
            }
        }
       	if (flag != null && flag == 'inv') {
            tpage = '2';
        } else if (flag != null && flag == 'mem') {
            tpage = '1';
        } else if (flag != null && flag == 'child') {
            tpage = '0';
        } else if (flag != null && flag == 'alt') {
            tpage = '1';
        }else if (flag != null && flag == 'pledge') {
            tpage = '0';
        }else if (flag != null && flag == 'mort') {
            tpage = '0';
        }else if (flag != null && flag == 'exc') {
            tpage = '1';
        }else if (flag != null && flag == 'serill') {
            tpage = '0';
        }else if (flag != null && flag == 'puun') {
            tpage = '0';
        }else if (flag != null && flag == 'spotCheck') {
            tpage = '0';
        }

        goShowNextFive(flag, tpage,CurrentFirstPage,totalPage);
    }
    function goShowNextFive(flag, n,CurrentFirstPage,totalPage) {
        var currentMaxPage = 0;
        if((CurrentFirstPage+4)<totalPage){
            currentMaxPage = CurrentFirstPage+4;
        } else{
            currentMaxPage = totalPage;
        }
        var request = new ajax.Request();
        if (flag != null && flag == 'inv') {
            var invPagination = document.getElementById("invPagination");
            invPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"inv\","+currentMaxPage+",2,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"ainv"+i+"\" href='javascript:goPage3(\"inv\","+i+");'><span id=\"spaninv"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"inv\","+currentMaxPage+",2,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            invPagination.innerHTML= innerHTML;
            goPage3("inv",CurrentFirstPage);
        }else if (flag != null && flag == 'mem') {
            var memPagination = document.getElementById("memPagination");
            memPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"mem\","+currentMaxPage+",1,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"amem"+i+"\" href='javascript:goPage3(\"mem\","+i+");'><span id=\"spanmem"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"mem\","+currentMaxPage+",1,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            memPagination.innerHTML= innerHTML;
            goPage3("mem",CurrentFirstPage);
        } else if (flag != null && flag == 'child') {
            var childPagination = document.getElementById("childPagination");
            childPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"child\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"achild"+i+"\" href='javascript:goPage3(\"child\","+i+");'><span id=\"spanchild"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"child\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            childPagination.innerHTML= innerHTML;
            goPage3("child",CurrentFirstPage);
        }else if (flag != null && flag == 'alt') {
            var altPagination = document.getElementById("altPagination");
            altPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"alt\","+currentMaxPage+",1,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"aalt"+i+"\" href='javascript:goPage3(\"alt\","+i+");'><span id=\"spanalt"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"alt\","+currentMaxPage+",1,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            altPagination.innerHTML= innerHTML;
            goPage3("alt",CurrentFirstPage);
        }else if (flag != null && flag == 'pledge') {
            var pledgePagination = document.getElementById("pledgePagination");
            pledgePagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"pledge\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"apledge"+i+"\" href='javascript:goPage9(\"pledge\","+i+");'><span id=\"spanpledge"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"pledge\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            pledgePagination.innerHTML= innerHTML;
            goPage9("pledge",CurrentFirstPage);
        }else if (flag != null && flag == 'mort') {
            var mortPagination = document.getElementById("mortPagination");
            mortPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"mort\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"amort"+i+"\" href='javascript:goPage10(\"mort\","+i+");'><span id=\"spanmort"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"mort\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            mortPagination.innerHTML= innerHTML;
            goPage10("mort",CurrentFirstPage);
        }else if (flag != null && flag == 'exc') {
            var excPagination = document.getElementById("excPagination");
            excPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"exc\","+currentMaxPage+",1,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"aexc"+i+"\" href='javascript:goPage6(\"exc\","+i+");'><span id=\"spanexc"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"exc\","+currentMaxPage+",1,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            excPagination.innerHTML= innerHTML;
            goPage6("exc",CurrentFirstPage);
        }else if (flag != null && flag == 'serill') {
            var serillPagination = document.getElementById("serillPagination");
            serillPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"serill\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"aserill"+i+"\" href='javascript:goPage3(\"serill\","+i+");'><span id=\"spanserill"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"serill\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            serillPagination.innerHTML= innerHTML;
            goPage3("serill",CurrentFirstPage);
        }else if (flag != null && flag == 'pun') {
            var punPagination = document.getElementById("punPagination");
            punPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"pun\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"apun"+i+"\" href='javascript:goPage5(\"pun\","+i+");'><span id=\"spanpun"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"pun\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            punPagination.innerHTML= innerHTML;
            goPage5("pun",CurrentFirstPage);
        }else if (flag != null && flag == 'spotCheck') {
            var spotCheckPagination = document.getElementById("spotCheckPagination");
            spotCheckPagination.innerHTML='';
            var innerHTML="<table cellpadding=\"0\" cellspacing=\"0\" class=\"detailsList\">"+
                "<th colspan=\"4\" style=\"text-align:right;\">";
            if(CurrentFirstPage==1){
                innerHTML += "<span style=\"color:blue\"><<</span>";
            }else{
                innerHTML += "<span><a href='javascript:slipFive(\"spotCheck\","+currentMaxPage+",0,\"pre\");'><<</a></span>";
            }
            for(var i=CurrentFirstPage;i<=currentMaxPage;i++){
                innerHTML += "    &nbsp;<a id=\"aspotCheck"+i+"\" href='javascript:goPage3(\"spotCheck\","+i+");'><span id=\"spanspotCheck"+i+"\">"+i+"</span></a>";
            }
            if(currentMaxPage==totalPage){
                innerHTML += "&nbsp;&nbsp;<span style=\"color:blue\">>></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }else{
                innerHTML += "&nbsp;&nbsp;<a href='javascript:slipFive(\"spotCheck\","+currentMaxPage+",0,\"next\");'><span>>></span></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+
                        "</th>"+
                        "</table>";
            }
            spotCheckPagination.innerHTML= innerHTML;
            goPage3("spotCheck",CurrentFirstPage);
        }

    }
function goPage4(flag, n) {
    var request = new ajax.Request();
    pageNo4 = n;
    setRed(flag, n);
    if (flag != null && flag == 'mem') {
        request.loadTextByGet("/QueryMemList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshMemList);
    } else if (flag != null && flag == 'child') {
        request.loadTextByGet("/QueryChildList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshChildList);
    }else if (flag != null && flag == 'alt') {
        request.loadTextByGet("/QueryAltList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshAltList);
    } else {
        request.loadTextByGet("/QueryInvList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776", refreshInvList);
    }

}
function goPage5(flag, n) {
    var request = new ajax.Request();
    pageNo5 = n;
    setRed(flag, n);
    request.loadTextByGet("/QueryPunList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776&ran="+Math.random(), refreshPunList);
}

function goPage6(flag, n) {
    var request = new ajax.Request();
    pageNo6 = n;
    setRed(flag, n);
    request.loadTextByGet("/QueryExcList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776&ran="+Math.random(), refreshExcList);
}


function refreshInvList(message) {
    var divTab = document.getElementById("invDiv");
    divTab.innerHTML = '';
    divTab.innerHTML = message.substr(1, message.length - 2);
}
function refreshMemList(message) {
    var memDiv = document.getElementById("memDiv");
    memDiv.innerHTML = '';
    memDiv.innerHTML = message.substr(1, message.length - 2);
}
function refreshChildList(message) {
    var childDiv = document.getElementById("childDiv");
    childDiv.innerHTML = '';
    childDiv.innerHTML = message.substr(1, message.length - 2);
}
function refreshAltList(message) {
    var altDiv = document.getElementById("altDiv");
    altDiv.innerHTML = '';
    altDiv.innerHTML = message.substr(1, message.length - 2);
    doExpand();
}
function refreshPunList(message) {
    var punDiv = document.getElementById("punDiv");
    punDiv.innerHTML = '';
    punDiv.innerHTML = message.substr(1, message.length - 2);
    doExpand_pun();
}
function refreshExcList(message) {
    var excDiv = document.getElementById("excDiv");
    excDiv.innerHTML = '';
    excDiv.innerHTML = message.substr(1, message.length - 2);
    doExpand_exc();
}
    function refreshSerillList(message) {
        var serillDiv = document.getElementById("serillDiv");
        serillDiv.innerHTML = '';
        serillDiv.innerHTML = message.substr(1, message.length - 2);
    }
    function refreshSpotCheckList(message) {
        var spotCheckDiv = document.getElementById("spotCheckDiv");
        spotCheckDiv.innerHTML = '';
        spotCheckDiv.innerHTML = message.substr(1, message.length - 2);
    }

function next1(flag) {
    var tpage = '2';
    if (flag != null && flag == 'mem') {
        tpage = '1';
    } else if (flag != null && flag == 'child') {
        tpage = '0';
    } else if (flag != null && flag == 'alt') {
        tpage = '1';
    }

    goPage1(flag, tpage);
}
function next2(flag) {
    var tpage = '2';
    if (flag != null && flag == 'mem') {
        tpage = '1';
    } else if (flag != null && flag == 'child') {
        tpage = '0';
    } else if (flag != null && flag == 'alt') {
        tpage = '1';
    }

    goPage2(flag, tpage);
}
function next3(flag) {
    var tpage = '2';
    if (flag != null && flag == 'mem') {
        tpage = '1';
    } else if (flag != null && flag == 'child') {
        tpage = '0';
    } else if (flag != null && flag == 'alt') {
        tpage = '1';
    }else if (flag != null && flag == 'serill') {
        tpage = '0';
    }else if (flag != null && flag == 'spotCheck') {
        tpage = '0';
    }

    goPage3(flag, tpage);
}
function next4(flag) {
    var tpage = '2';
    if (flag != null && flag == 'mem') {
        tpage = '1';
    } else if (flag != null && flag == 'child') {
        tpage = '0';
    } else if (flag != null && flag == 'alt') {
        tpage = '1';
    }

    goPage4(flag, tpage);
}
function next5(flag) {
    var tpage = '0';
    goPage5(flag, tpage);
}
function next6(flag) {
    var tpage = '1';
    goPage6(flag, tpage);
}



function pre1(flag) {
    goPage1(flag, 1);
}
function pre2(flag) {
    goPage2(flag, 1);
}
function pre3(flag) {
    goPage3(flag, 1);
}
function pre4(flag) {
    goPage4(flag, 1);
}
function pre5(flag) {
    goPage5(flag, 1);
}
function pre6(flag) {
    goPage6(flag, 1);
}


    function setRed(flag, n) {
        var currentFirstPage = Math.ceil(n/5)*5-4;
        var tpage = '2';
        if (flag != null && flag == 'inv') {
            tpage = '2';
        }else if (flag != null && flag == 'mem') {
            tpage = '1';
        } else if (flag != null && flag == 'child') {
            tpage = '0';
        } else if (flag != null && flag == 'alt') {
            tpage = '1';
        }else if (flag != null && flag == 'pun') {
            tpage = '0';
        }else if (flag != null && flag == 'exc') {
            tpage = '1';
        }else if (flag != null && flag == 'pledge') {
            tpage = '0';
        } else if (flag != null && flag == 'mort') {
            tpage = '0';
        }else if (flag != null && flag == 'serill') {
            tpage = '0';
        } else if (flag != null && flag == 'spotCheck') {
            tpage = '0';
        }

        for (var i = currentFirstPage; i <= (currentFirstPage+4); i++) {
            if(i>tpage){

            }else{
                document.getElementById("span" + flag + i).style.color = "";
                document.getElementById("a" + flag + i).style.textDecoration = "underline";
            }
        }
        document.getElementById("span" + flag + n).style.color = "red";
        document.getElementById("a" + flag + n).style.textDecoration = "none";
    }

var pageNo9 = 1;//股权出质
function goPage9(flag, n) {
    var request = new ajax.Request();
    pageNo9 = n;
    setRed(flag, n);
    request.loadTextByGet("/QueryPledgeList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776&ran=" + Math.random(), refreshPledgeList);
}

function next9(flag) {
    var tpage = '0';
    goPage9(flag, tpage);
}

function pre9(flag) {
    goPage9(flag, 1);
}

function refreshPledgeList(message) {
    var pledgeDiv = document.getElementById("pledgeDiv");
    pledgeDiv.innerHTML = '';
    pledgeDiv.innerHTML = message.substr(1, message.length - 2);
}

var pageNo10 = 1;//动产抵押
function goPage10(flag, n) {
    var request = new ajax.Request();
    pageNo10 = n;
    setRed(flag, n);
    request.loadTextByGet("/QueryMortList.jspx?pno=" + n + "&mainId=C0E2ED0898EBC82FD7567EC589AC9776&ran=" + Math.random(), refreshMortList);
}

function next10(flag) {
    var tpage = '0';
    goPage10(flag, tpage);
}

function pre10(flag) {
    goPage10(flag, 1);
}

function refreshMortList(message) {
    var mortDiv = document.getElementById("mortDiv");
    mortDiv.innerHTML = '';
    mortDiv.innerHTML = message.substr(1, message.length - 2);
}
 //显示更多
    function showAlterMore(rowIndex,size){
        var a = document.getElementById("a"+rowIndex);
        var td = document.getElementById("td"+rowIndex);
        var detailTd = document.getElementById("detailTd"+rowIndex);
        var div = document.getElementById("xingzhengchufa");
        var ele = document.getElementById("7");
        var showDiv1 = document.getElementById("tr"+rowIndex+1);
        if(showDiv1.style.display=="none"){
            a.innerText="收起更多";
            td.rowSpan=size+1;
            detailTd.rowSpan=size+1;
        }else{
             a.innerText="更多";
             td.rowSpan = 2;
             detailTd.rowSpan = 2;
             changeStyle('tabs',ele);
             if(div.style.display="block"){
                div.style.display="";
             }else{
                 div.style.display="block";
             }
        }

        for(var i=1;i<size;i++){
            var showDiv = document.getElementById("tr"+rowIndex+i);
            if(showDiv.style.display=="none"){
                   showDiv.style.display="";
                }else{
                   showDiv.style.display="none";
                }
        }

    }
/*经营异常展开、缩起*/
    var arr_excIn = new Array();
    var arr_excOut = new Array();
    /*展开内容*/
    doExpand_exc();
/*变更信息展开、缩起*/
    var arr_altBe = new Array();
    var arr_altAf = new Array();
    /*展开内容*/
    doExpand();

/*行政处罚 内容展开、收起*/
    var arr_punBasis = new Array();
    var arr_punResult = new Array();
    var arr_punAlt = new Array();

</script>
'''

enterprise_html_lilezhongguo = '''

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=GBK" />

<title>全国企业信用信息公示系统</title>
<link href="framework/China/css/public3.css" type="text/css" rel="stylesheet" />
<link rel="stylesheet" href="framework/China/css/style.css" type="text/css" media="screen" charset="utf-8"/>
<script type="text/javascript">
var index = 0;

function _pageTo(name,start,end,_index){
	var aa = 0;
	 index = _index;
	var fr = document.getElementsByTagName("tr");
	for(var i=0;i<fr.length;i++){
		if(fr[i].getAttribute('name')==name){
			aa++;
			if(aa<=end &&  aa >start){
				fr[i].style.display = "";
			}else{
				fr[i].style.display = "none";
			}
		}
	}
}
function _pageUp(name){
	if(index==1){

	}else{
		_pageTo(name,(index-2)*5,(index-1)*5,index-1);
	}

}
function _pageDown(name,totalPage){
	if(index == Math.floor(totalPage)){
	}else{
		_pageTo(name,(index)*5,(index+1)*5,index+1);
	}

}
var index_10 = 0;

function _pageTo_10(name,start,end,_index){
	var aa = 0;
	 index_10 = _index;
	var fr = document.getElementsByTagName("tr");
	for(var i=0;i<fr.length;i++){
		if(fr[i].getAttribute('name')==name){
			aa++;
			if(aa<=end &&  aa >start){
				fr[i].style.display = "";
			}else{
				fr[i].style.display = "none";
			}
		}
	}
}
function _pageUp_10(name){
	if(index_10==1){

	}else{
		_pageTo_10(name,(index_10-2)*10,(index_10-1)*10,index_10-1);
	}

}
function _pageDown_10(name,totalPage){
	if(index_10 == Math.floor(totalPage)){
	}else{
		_pageTo_10(name,(index_10)*10,(index_10+1)*10,index_10+1);
	}

}

var indexFor3 = 0;
var indeOld = 0;

function _pageToFor3(name,start,end,_index){
	var aa = 0;
	indeOld = indexFor3;
	 indexFor3 = _index;
	var fr = document.getElementsByTagName("tr");
	for(var i=0;i<fr.length;i++){
		if(fr[i].getAttribute('name')==name){
			aa++;
			if(aa<=end &&  aa >start){
				fr[i].style.display = "";
			}else{
				fr[i].style.display = "none";
			}
		}

	}

	var fr = document.getElementsByTagName("a");
	for(var i=0;i<fr.length;i++){
		if(fr[i].getAttribute('name')==name+"_a"){
				if(fr[i].id=="bg_"+_index){
					fr[i].className = "_on";
				}else{
					fr[i].className = "";
				}
			}
		}

}
function _pageUpFor3(name){
	if(indexFor3==1){

	}else{
		_pageToFor3(name,0,3,1);
		ScrollImgLeft1();
	}

}
function _pageDownFor3(name,totalPage){
	if(indexFor3 == Math.floor(totalPage)){
	}else{
		_pageToFor3(name,(Math.floor(totalPage)-1)*3,(Math.floor(totalPage))*3,Math.floor(totalPage));
		ScrollImgLeft2();
	}

}


function ScrollImgLeft(){
	var speed=1
	var scroll_begin = document.getElementById("scroll_begin");
	var scroll_end = document.getElementById("scroll_end");
	var scroll_div = document.getElementById("scroll_div");
	Marquee();

}


function Marquee(){
		if(indeOld <= indexFor3){
			//if(scroll_div.scrollLeft>=10*indexFor3)){
			//	clearInterval(MyMar);
			//	return ;
			//}else{
				scroll_div.scrollLeft = scroll_div.scrollLeft + 21*(indexFor3-indeOld);
				return;
			//}
		}else{
				scroll_div.scrollLeft = scroll_div.scrollLeft - 21*(indeOld-indexFor3);
				return ;
		}

		}
function ScrollImgLeft2(){
	var speed=1
	var scroll_begin = document.getElementById("scroll_begin");
	var scroll_end = document.getElementById("scroll_end");
	var scroll_div = document.getElementById("scroll_div");
	Marquee2();

}


function Marquee2(){
		scroll_div.scrollLeft = scroll_div.scrollLeft + 10000;
}
function ScrollImgLeft1(){
	var speed=1
	var scroll_begin = document.getElementById("scroll_begin");
	var scroll_end = document.getElementById("scroll_end");
	var scroll_div = document.getElementById("scroll_div");
	//scroll_end.innerHTML=scroll_begin.innerHTML
	//scroll_div.scrollLeft = 0;

	//scroll_div.onmouseover=function() {clearInterval(MyMar)}
	//scroll_div.onmouseout=function() {MyMar=setInterval(Marquee,speed)}
	Marquee1();

}


function Marquee1(){
				scroll_div.scrollLeft = scroll_div.scrollLeft - 10000;
		}

function _openPage(url) {
    var dynamicForm = document.createElement("form");
    document.body.appendChild(dynamicForm);
    var paraString = url.substring(url.indexOf("?")+1,url.length).split("&");
    var actionString = url.substring(0,url.indexOf("?"));
	var paraObj = {}
	for (i=0; j=paraString[i]; i++){
		paraObj[j.substring(0,j.indexOf("=")).toLowerCase()] = j.substring(j.indexOf
		("=")+1,j.length);
	}
    dynamicForm.method = 'post';
    dynamicForm.action = actionString
    dynamicForm.target = '_blank';
    dynamicForm.innerHTML="";
	for ( var p in paraObj ){
	  	var newElement = document.createElement("input");
	    newElement.setAttribute("name",p);
	    newElement.setAttribute("type","hidden");
	    newElement.setAttribute("value",paraObj[p]);
	    dynamicForm.appendChild(newElement);
	}
	dynamicForm.submit();
}
function _openPageForSelf(url) {
    var dynamicForm = document.createElement("form");
    document.body.appendChild(dynamicForm);
    var paraString = url.substring(url.indexOf("?")+1,url.length).split("&");
    var actionString = url.substring(0,url.indexOf("?"));
	var paraObj = {}
	for (i=0; j=paraString[i]; i++){
		paraObj[j.substring(0,j.indexOf("=")).toLowerCase()] = j.substring(j.indexOf
		("=")+1,j.length);
	}
    dynamicForm.method = 'post';
    dynamicForm.action = actionString
    dynamicForm.target = '_self';
    dynamicForm.innerHTML="";
	for ( var p in paraObj ){
	  	var newElement = document.createElement("input");
	    newElement.setAttribute("name",p);
	    newElement.setAttribute("type","hidden");
	    newElement.setAttribute("value",paraObj[p]);
	    dynamicForm.appendChild(newElement);
	}
	dynamicForm.submit();
}

<!-- 新分页函数 -->
function _pageToNew(name,pageSize,pageNo){
	//每页显示条数
	pageSize = Number(pageSize);
	//当前页码
	pageNo = Number(pageNo);
	//总页数
	totalPage = Math.floor(document.getElementById("totalPage_"+name).value);

	//当前页码隐藏域赋值
	if(document.getElementById("currentPageNo_"+name)){
		document.getElementById("currentPageNo_"+name).value=pageNo;
	}
	//显示表格行
	showTableTr(name,pageNo*pageSize-pageSize,pageNo*pageSize);

	if(totalPage<=10){
		showPageSpan(name,1,totalPage);
	}else{
		if(pageNo<10){
			showPageSpan(name,1,10);
		}else if(pageNo+4>totalPage){
			showPageSpan(name,totalPage-9,totalPage);
		}else{
			showPageSpan(name,pageNo-5,pageNo+4);
		}
	}

	//将当前页码变成红色
	for(j=0;j<=totalPage;j++){
		if(document.getElementById(name+"_a_"+j)){
			if(j==pageNo){
				document.getElementById(name+"_a_"+j).style.color="red";
			}else{
				document.getElementById(name+"_a_"+j).style.color="";
			}
		}
	}

}

//上一页
function _pageUpNew(name,pageSize){
	var pageNo = Math.round(document.getElementById("currentPageNo_"+name).value);
	if(pageNo>1){
		pageNo = pageNo-1;
	}else{
		pageNo= 1;
	}
	_pageToNew(name,pageSize,pageNo);
}

//下一页
function _pageDownNew(name,pageSize){
	var pageNo = Math.round(document.getElementById("currentPageNo_"+name).value);
	//总页数
	var totalPage = Math.floor(document.getElementById("totalPage_"+name).value);

	if(pageNo+1>totalPage){
		_pageToNew(name,pageSize,pageNo);
	}else{
		_pageToNew(name,pageSize,pageNo+1);
	}
}

function showPageSpan(name,startNo,endNo){

	//隐藏所有分页符
	var fr = document.getElementById("table_"+name).getElementsByTagName("span");
	for(var t=0;t<fr.length;t++){
		if(fr[t].getAttribute('name')=="span_"+name){
			fr[t].style.display = "none";
		}
	}

	//显示十个分页符
	for(i=startNo;i<=endNo;i++){
		if(document.getElementById(name+"_"+i)){
			document.getElementById(name+"_"+i).style.display="";
		}
	}

}

function showTableTr(name,startNo,endNo){
	//隐藏当前表格所有行
	var fr = document.getElementById("table_"+name).getElementsByTagName("tr");
	for(var z=0;z<fr.length;z++){
		if(fr[z].getAttribute('name')==name){
			fr[z].style.display = "none";
		}
	}
	//显示当前页的行		/*xd.liu 2014-09-06 14:57 修改翻页代码 ，页面上有2个list中的tr * /
	for(i=startNo+1;i<=endNo;i++){
		if(document.getElementById("tr_"+name+"_"+i)){
			document.getElementById("tr_"+name+"_"+i).style.display="";
		}
		if(document.getElementById("tr_"+name+"2_"+i)){
			document.getElementById("tr_"+name+"2_"+i).style.display="";
		}
	}
}

</script>
<style>
.scroll_div {width:600px; height:49px;margin:0 auto; overflow: hidden; white-space: nowrap; background:#ffffff;float:left}
#scroll_begin, #scroll_end, #scroll_begin ul, #scroll_end ul, #scroll_begin ul li, #scroll_end ul li{display:inline;}
._on{font-weight:bold;}
</style>
<script type="text/javascript">


function r0(){
document.getElementById('jibenxinxi').style.display='block';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('yichangminglu').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r2(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='block';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('yichangminglu').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r3(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='block';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('yichangminglu').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r4(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('yichangminglu').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('guquanchuzhi').style.display='block';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r5(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='block';
document.getElementById('yichangminglu').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r6(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('yichangminglu').style.display='block';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r7(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('chouchaxinxi').style.display='block';
document.getElementById('yichangminglu').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r8(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='block';
document.getElementById('yichangminglu').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r9(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('sipinyixie').style.display='block';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r30(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='block';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r31(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='block';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r32(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='block';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r33(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='block';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='none';
}
function r10(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='block';
document.getElementById('jianyanjianche').style.display='none';
}
function r11(){
document.getElementById('jibenxinxi').style.display='none';
document.getElementById('beian').style.display='none';
document.getElementById('gsgsxx_xzcf').style.display='none';
document.getElementById('guquanchuzhi').style.display='none';
document.getElementById('dongchandiya').style.display='none';
document.getElementById('chouchaxinxi').style.display='none';
document.getElementById('yanzhongweifa').style.display='none';
document.getElementById('sipinyixie').style.display='none';
document.getElementById('jcxxfj').style.display='none';
document.getElementById('yjxx').style.display='none';
document.getElementById('jsxx').style.display='none';
document.getElementById('tsxx').style.display='none';
document.getElementById('xiaofeizhetousujubao').style.display='none';
document.getElementById('jianyanjianche').style.display='block';
}
function t1(){
  document.getElementById('qynb').style.display='block';
  document.getElementById('xzxk').style.display='none';
  document.getElementById('zzcq').style.display='none';
  document.getElementById('tzrxx').style.display='none';
  document.getElementById('xzcf').style.display='none';
  document.getElementById('tzrbgxx').style.display='none';
}
function t2(){
  document.getElementById('qynb').style.display='none';
  document.getElementById('xzxk').style.display='block';
  document.getElementById('zzcq').style.display='none';
  document.getElementById('tzrxx').style.display='none';
  document.getElementById('xzcf').style.display='none';
  document.getElementById('tzrbgxx').style.display='none';
}
function t3(){
  document.getElementById('qynb').style.display='none';
  document.getElementById('xzxk').style.display='none';
  document.getElementById('zzcq').style.display='block';
  document.getElementById('tzrxx').style.display='none';
  document.getElementById('tzrbgxx').style.display='none';
  document.getElementById('xzcf').style.display='none';
}
function t4(){
  document.getElementById('qynb').style.display='none';
  document.getElementById('xzxk').style.display='none';
  document.getElementById('zzcq').style.display='none';
  document.getElementById('tzrxx').style.display='block';
  document.getElementById('xzcf').style.display='none';
  document.getElementById('tzrbgxx').style.display='none';
}
function t5(){
  document.getElementById('qynb').style.display='none';
  document.getElementById('xzxk').style.display='none';
  document.getElementById('zzcq').style.display='none';
  document.getElementById('tzrxx').style.display='none';
  document.getElementById('xzcf').style.display='block';
  document.getElementById('tzrbgxx').style.display='none';
}
function t6(){
  document.getElementById('qynb').style.display='none';
  document.getElementById('xzxk').style.display='none';
  document.getElementById('zzcq').style.display='none';
  document.getElementById('tzrbgxx').style.display='block';
  document.getElementById('xzcf').style.display='none';
}

function togo(str){
  if(str=='1'){
     document.getElementById('detailsCon_gs').style.display='block';
     document.getElementById('detailsCon_qy').style.display='none';
     document.getElementById('detailsCon_qt').style.display='none';
     document.getElementById('detailsCon_sf').style.display='none';
 	 document.getElementById('detailsCon_jb').style.display='none';
  }else if(str=='2'){
     document.getElementById('detailsCon_gs').style.display='none';
     document.getElementById('detailsCon_qy').style.display='block';
     document.getElementById('detailsCon_qt').style.display='none';
     document.getElementById('detailsCon_sf').style.display='none';
 	 document.getElementById('detailsCon_jb').style.display='none';
  }else if(str=='3'){
     document.getElementById('detailsCon_gs').style.display='none';
     document.getElementById('detailsCon_qy').style.display='none';
     document.getElementById('detailsCon_qt').style.display='block';
     document.getElementById('detailsCon_sf').style.display='none';
 	 document.getElementById('detailsCon_jb').style.display='none';
  }else if(str=='4'){
     document.getElementById('detailsCon_gs').style.display='none';
     document.getElementById('detailsCon_qy').style.display='none';
     document.getElementById('detailsCon_qt').style.display='none';
     document.getElementById('detailsCon_sf').style.display='block';
 	 document.getElementById('detailsCon_jb').style.display='none';
  }else if(str=='5'){
 		document.getElementById('detailsCon_gs').style.display='none';
 		document.getElementById('detailsCon_qy').style.display='none';
 		document.getElementById('detailsCon_qt').style.display='none';
 		document.getElementById('detailsCon_sf').style.display='none';
 		document.getElementById('detailsCon_jb').style.display='block';
	}
}

function s1(){
  document.getElementById('guquandongjie').style.display='block';
  document.getElementById('gudongbiangeng').style.display='none';
}

function s2(){
  document.getElementById('guquandongjie').style.display='none';
  document.getElementById('gudongbiangeng').style.display='block';
}

function t20(){
  document.getElementById('qyxyblxx').style.display='block';
  document.getElementById('qyxylhxx').style.display='none';
}
function t21(){
  document.getElementById('qyxyblxx').style.display='none';
  document.getElementById('qyxylhxx').style.display='block';
}

function qygs1(){
  document.getElementById('sifapanding').style.display='block';
}


function q1(){
  document.getElementById('xingzhengxuke').style.display='block';
  document.getElementById('xingzhengchufa').style.display='none';
  document.getElementById('shengchananquanshigu').style.display='none';
}
function q2(){
  document.getElementById('xingzhengxuke').style.display='none';
  document.getElementById('xingzhengchufa').style.display='block';
  document.getElementById('shengchananquanshigu').style.display='none';
}
function q3(){
  document.getElementById('xingzhengxuke').style.display='none';
  document.getElementById('xingzhengchufa').style.display='none';
  document.getElementById('shengchananquanshigu').style.display='block';
}
</script>

<script type="text/javascript" defer="defer">
 function changeStyle(divId,ele){
            var liAry=document.getElementById(divId).getElementsByTagName("li");
            var liLen=liAry.length;
            var liID=ele;
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

  function ShowSpan(obj,n){
   var span = obj.parentNode.getElementsByTagName("tabs");
   for(var i=0;i<span.length;i++){
     span[i].className = "current";
   }
   span[n].className = "";
   var li = obj.parentNode.getElementsByTagName("li")
   li[n].className = "current";
   for(var i=0;i<li.length;i++){
    if(i!=n){
      li[i].className = "";
    }
    li[i].onmouseout = function(){
      this.className = "current";
    }
   }
  }
function _load(){
  var czmk = "czmk0";
  if(czmk=="czmk0"){
    r0();changeStyle('tabs','0');

  }else if(czmk=="czmk2"){
    r2();changeStyle('tabs','2');






  }else if(czmk=="czmk3"){
    r3();changeStyle('tabs','3');
  }else if(czmk=="czmk4"){
    r4();changeStyle('tabs','4');
  }else if(czmk=="czmk5"){
    r5();changeStyle('tabs','5');
  }else if(czmk=="czmk6"){
    r6();changeStyle('tabs','6');
  }else if(czmk=="czmk7"){
    r7();changeStyle('tabs','7');
  }else if(czmk=="czmk14"){//严重违法
    r8();changeStyle('tabs','8');
  }else if(czmk=="czmk8"){
    togo('2');//大栏目内容隐藏显示
    t1();//小栏目显示内容
    changeStyle('qygsTabs','qygs_qynb');//小栏目内容样式选中
    changeStyle('leftTabs','gs2');//大栏目样式选中
  }else if(czmk=="czmk19"){
    r9();changeStyle('tabs','9');

  }else if(czmk=="czmk9"){
    togo('3');
    q1();
    changeStyle('leftTabs','gs3');
    changeStyle('qtbmgsTabs','qtbm_xzxk');
  }else if(czmk=="czmk30"){
		r30();
		changeStyle('tabs','30');
  }else if(czmk=="czmk31"){
		r31();
		changeStyle('tabs','31');
  }else if(czmk=="czmk32"){
		r32();
		changeStyle('tabs','32');
  }else if(czmk=="czmk33"){
		r33();
		changeStyle('tabs','33');
  }else if(czmk=="czmk10"){
    togo('2');t2();changeStyle('leftTabs','gs2');changeStyle('qygsTabs','qygs_xzxk');
  }else if(czmk=="czmk11"){
    togo('2');t3();changeStyle('leftTabs','gs2');changeStyle('qygsTabs','qygs_zzcq');
  }else if(czmk=="czmk12"){
    togo('2');t4();changeStyle('leftTabs','gs2');changeStyle('qygsTabs','qygs_tzrxx');
  }else if(czmk=="czmk13"){
    togo('2');t5();changeStyle('leftTabs','gs2');changeStyle('qygsTabs','qygs_xzcf');
  }else if(czmk=="czmk16"){
    togo('3');
    q2();
    changeStyle('leftTabs','gs3');
    changeStyle('qtbmgsTabs','qtbm_xzcf');
  }else if(czmk=="czmk34"){
    togo('3');
    q3();
    changeStyle('leftTabs','gs3');
    changeStyle('qtbmgsTabs','qtbm_scaqsg');
  }else if(czmk=="czmk15"){
    togo('2');//大栏目内容隐藏显示
    t6();//小栏目显示内容
    changeStyle('qygsTabs','qygs_tzrbgxx');//小栏目内容样式选中
    changeStyle('leftTabs','gs2');//大栏目样式选中
  }else if(czmk=="czmk17"){//司法协助_股权冻结
    togo('4');//大栏目内容隐藏显示
    s1();
    changeStyle('sfxzgsTabs','sfxz_gqdj');//小栏目内容样式选中
    changeStyle('leftTabs','gs4');//大栏目样式选中
  }else if(czmk=="czmk18"){//司法协助_股东变更
    togo('4');//大栏目内容隐藏显示
    s2();
    changeStyle('sfxzgsTabs','sfxz_gqbg');//小栏目内容样式选中
    changeStyle('leftTabs','gs4');//大栏目样式选中
  }else if(czmk=="czmk20"){//消费者投诉举报
		//togo('5');//大栏目内容隐藏显示
		//o1();
		//changeStyle('xfztsjbTabs','xfztsjb');//小栏目内容样式选中
		//changeStyle('leftTabs','gs5');//大栏目样式选中
		r10();changeStyle('tabs','10');
  }else if(czmk=="czmk22"){//检验检测
		//togo('5');//大栏目内容隐藏显示
		//o3();
		//changeStyle('xfztsjbTabs','jyjc');//小栏目内容样式选中
		//changeStyle('leftTabs','gs5');//大栏目样式选中
		r11();changeStyle('tabs','11');
	}
  //_pageTo('bl',0,5,1);
  //_pageTo('lh',0,5,1);
}
function doChange(id){
  if(id=="0"){
    var src="ztxy.do?method=qyInfo&maent.pripid=5100004000001311&czmk=czmk1&from=&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="2"){
    var src="ztxy.do?method=baInfo&maent.pripid=5100004000001311&czmk=czmk2&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="3"){
    var src="ztxy.do?method=cfInfo&maent.pripid=5100004000001311&czmk=czmk3&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="4"){
    var src="ztxy.do?method=gqczxxInfo&maent.pripid=5100004000001311&czmk=czmk4&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="5"){
    var src="ztxy.do?method=dcdyInfo&maent.pripid=5100004000001311&czmk=czmk4&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="6"){
    var src="ztxy.do?method=jyycInfo&maent.pripid=5100004000001311&czmk=czmk6&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="7"){
    var src="ztxy.do?method=ccjcInfo&maent.pripid=5100004000001311&czmk=czmk7&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="8"){
    var src="ztxy.do?method=yzwfInfo&maent.pripid=5100004000001311&czmk=czmk14&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="9"){
    var src="ztxy.do?method=spyzInfo&maent.pripid=5100004000001311&czmk=czmk19&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="30"){
    var src="ztxy.do?method=JcxxfjInfo&maent.pripid=5100004000001311&czmk=czmk30&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="31"){
    var src="ztxy.do?method=YjxxInfo&maent.pripid=5100004000001311&czmk=czmk31&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="32"){
    var src="ztxy.do?method=JsxxInfo&maent.pripid=5100004000001311&czmk=czmk32&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="33"){
    var src="ztxy.do?method=TsxxInfo&maent.pripid=5100004000001311&czmk=czmk33&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="10"){
		var src="ztxy.do?method=xfztsjbInfo&maent.pripid=5100004000001311&czmk=czmk20&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="11"){
		var src="ztxy.do?method=jyjcInfo&maent.pripid=5100004000001311&czmk=czmk22&random="+new Date().getTime();
       _openPageForSelf(src);
  }
}
function doPageDown(id){
  if(id=='gs1'){
    var src="ztxy.do?method=qyInfo&maent.pripid=5100004000001311&czmk=czmk1&from=&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=='gs2'){
    var src="ztxy.do?method=qygsInfo&maent.pripid=5100004000001311&czmk=czmk8&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=='gs3') {
    var src="ztxy.do?method=qtgsInfo&maent.pripid=5100004000001311&czmk=czmk9&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=='gs4'){
    var src="ztxy.do?method=sfgsInfo&maent.pripid=5100004000001311&czmk=czmk17&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=='gs5'){
		var src="ztxy.do?method=xfztsjbInfo&maent.pripid=5100004000001311&czmk=czmk20&random="+new Date().getTime();
       _openPageForSelf(src);
	}
}


function o1(){
	document.getElementById('xiaofeizhetousujubao').style.display='block';
	document.getElementById('jianyanjianche').style.display='none';
}

function o3(){
	document.getElementById('xiaofeizhetousujubao').style.display='none';
	document.getElementById('jianyanjianche').style.display='block';
}

function doPageRight(id){
  if(id=='qygs_qynb'){
    var src="ztxy.do?method=qygsInfo&maent.pripid=5100004000001311&czmk=czmk8&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=='qygs_xzxk'){
    var src="ztxy.do?method=qygsForXzxkInfo&maent.pripid=5100004000001311&czmk=czmk10&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=='qygs_zzcq'){
    var src="ztxy.do?method=qygsForZzcqInfo&maent.pripid=5100004000001311&czmk=czmk11&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=='qygs_tzrxx'){
    var src="ztxy.do?method=qygsForTzrxxInfo&maent.pripid=5100004000001311&czmk=czmk12&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=='qygs_xzcf'){
    var src="ztxy.do?method=qygsForXzcfInfo&maent.pripid=5100004000001311&czmk=czmk13&random="+new Date().getTime();
       _openPageForSelf(src);
  }
  /** xd.liu 2014-09-02 17:07 新增发起人股权变更信息 */
  else if(id=="qygs_tzrbgxx"){
    var src="ztxy.do?method=qygsForTzrbgxxInfo&maent.pripid=5100004000001311&czmk=czmk15&random="+new Date().getTime();
       _openPageForSelf(src);
  }
}
function doPageLeft(id){
  if(id=="xzxk"){
    var src="ztxy.do?method=qtgsInfo&maent.pripid=5100004000001311&czmk=czmk9&random="+new Date().getTime();
       _openPageForSelf(src);
  }else if(id=="scaqsg"){
    var src="ztxy.do?method=qtgsScaqsgInfo&maent.pripid=5100004000001311&czmk=czmk34&random="+new Date().getTime();
       _openPageForSelf(src);
  }else{
    var src="ztxy.do?method=qtgsForCfInfo&maent.pripid=5100004000001311&czmk=czmk16&random="+new Date().getTime();
       _openPageForSelf(src);
  }
}

function doPageLeftForGq(id){
  if(id == "gqdj"){
    var src="ztxy.do?method=sfgsInfo&maent.pripid=5100004000001311&czmk=czmk17&random="+new Date().getTime();
       _openPageForSelf(src);
  }else{
    var src="ztxy.do?method=sfgsbgInfo&maent.pripid=5100004000001311&czmk=czmk18&random="+new Date().getTime();
       _openPageForSelf(src);
  }
}

function doDcdyDetail(morregid){
  var src = "ztxy.do?method=dcdyDetail&maent.pripid=5100004000001311&maent.xh="+morregid+"&random="+new Date().getTime();
  _openPage(src);
}

function beforeLess2(i){
  document.getElementById('beforeLess2_'+i).style.display='none';
  document.getElementById('beforeMore2_'+i).style.display='block';
}
function beforeMore2(i){
  document.getElementById('beforeLess2_'+i).style.display='block';
  document.getElementById('beforeMore2_'+i).style.display='none';
}
function beforeLess21(i){
  document.getElementById('beforeLess21_'+i).style.display='none';
  document.getElementById('beforeMore21_'+i).style.display='block';
}
function beforeMore21(i){
  document.getElementById('beforeLess21_'+i).style.display='block';
  document.getElementById('beforeMore21_'+i).style.display='none';
}
function doNdbg(nd){
  var src = "ztxy.do?method=ndbgDetail&maent.pripid=5100004000001311&maent.nd="+nd+"&random="+new Date().getTime();
  _openPage(src);
}
function doGqcx(licid){
  var src = "ztxy.do?method=gqczxxDetail&maent.pripid=5100004000001311&maent.xh="+licid+"&random="+new Date().getTime();
  _openPage(src);
}
/*
  xd.liu 2014-08-28 17:27 增加撤销、注销详情
*/
function doGqCxDetail(licid){
  var src = "ztxy.do?method=gqczxxZxDetail&maent.pripid=5100004000001311&maent.lx=C&maent.xh="+licid+"&random="+new Date().getTime();
  _openPage(src);
}
function doGqZxDetail(licid){
  var src = "ztxy.do?method=gqczxxZxDetail&maent.pripid=5100004000001311&maent.lx=X&maent.xh="+licid+"&random="+new Date().getTime();
  _openPage(src);
}
function doZscqDetail(xh,lx){
  var src = "ztxy.do?method=zscqDetail&maent.pripid=5100004000001311&maent.xh="+xh+"&maent.lx="+lx+"&random="+new Date().getTime();
  _openPage(src);
}
/*
  xd.liu 2014-09-03 13:47 行政许可文件详情
*/
function doXkxkDetail(nbxh,xh,lx){
  var src = "ztxy.do?method=doXkxkDetail&maent.pripid="+nbxh+"&maent.xh="+xh+"&maent.lx="+lx+"&random="+new Date().getTime();
  _openPage(src);
}
/**
  xd.liu 2014-09-05 16:10 国家局0822文档，行政处罚信息增加详情
*/
function doXzfyDetail(nbxh,ajbh){
  var src = "ztxy.do?method=doXzfyDetail&maent.pripid="+nbxh+"&maent.xh="+ajbh+"&random="+new Date().getTime();
  _openPage(src);
}
/**
  pf.zhu 2016-01-28 异地案件
*/
function doXzfyDetail2(nbxh,ajbh){
  var src = "ztxy.do?method=doXzfyDetail_yd&maent.pripid="+nbxh+"&maent.xh="+ajbh+"&random="+new Date().getTime();
  _openPage(src);
}
/*
  xd.liu 2015-01-07 10:24 司法协助股东变更详情
*/
function _doSfgqbgDetail(id){
  var src = "ztxy.do?method=doGqdjbgDetail&maent.pripid=5100004000001311&maent.xh="+id+"&random="+new Date().getTime();
  _openPage(src);
}
/*
  xd.liu 2015-01-07 10:24 司法协助股权冻结详情
*/
function _doSfgqdjDetail(id){
  var src = "ztxy.do?method=doGqdjDetail&maent.pripid=5100004000001311&maent.xh="+id+"&random="+new Date().getTime();
  _openPage(src);
}
function doPageLeftOther(id){
	if(id=="xfztsjb"){
		var src="ztxy.do?method=xfztsjbInfo&maent.pripid=5100004000001311&czmk=czmk20&random="+new Date().getTime();
       _openPageForSelf(src);
	}else{
		var src="ztxy.do?method=jyjcInfo&maent.pripid=5100004000001311&czmk=czmk22&random="+new Date().getTime();
       _openPageForSelf(src);
	}
}
function qtgsxxDetail(newsid,flag){
	var src="ztxy.do?method=qtgsxxDetail&newsid="+newsid+"&flag="+flag+"&random="+new Date().getTime();
	_openPage(src);
}

function _doXzxkDetail(xh){
  var src = "ztxy.do?method=doXzxkDetail&maent.pripid=5100004000001311&maent.xh="+xh+"&random="+new Date().getTime();
  _openPage(src);
}
function _doXzcfDetail(xh){
  var src = "ztxy.do?method=doXzcfDetail&maent.pripid=5100004000001311&maent.xh="+xh+"&random="+new Date().getTime();
  _openPage(src);
}
</script>

</head>
<!-- onload="_pageTo('fr_11_2',0,5,1);_pageTo('fr_11_1',0,5,1);_pageTo('fr_11_3',0,5,1);_pageTo('fr',0,5,1);_pageToFor3('bg',0,3,1);" -->
<body onload="_load();">
<input type="hidden" name="entname" value="利乐中国有限公司成都办事处" />
<input type="hidden" name="regno" value="企外川驻字第00070号"/>
<input type="hidden" name="entbigtype" value="23"/>
<div id="header">

<div class="top_sichuan">
	<div class="top-a"><a onclick="window.location='http://gsxt.saic.gov.cn';" style="cursor:pointer;">全国首页</a>
		<a href="ztxy.do?method=index&random=147852369874" style="cursor:pointer;">地方局首页</a>
	</div>
	<div class="top-a"><a href="###"  onclick="bszn.style.display='block'" style="cursor:pointer;">办事指南</a></div>
</div>
<!-- pf.zhu 2015-03-31 10:54 增加遂宁版本 -->

<div id="bszn" style="position:relative;display:none;">
<div class="abc_upload_box" style="display:block;position:absolute;left:315px;top:100px;">
     <div class="abc_upload_title">办事指南<a href="#" onclick="bszn.style.display='none'"></a></div>
     <div class="abc_upload_content">
          <ul>
              <li>
                  <span class="arrow"></span>
                  <a class="name"  href="ztxy.do?method=downLoadDoc&lx=0&random=174154551731">企业信用信息公示系统操作手册</a>
              </li>
              <li class="color_f5f5f5">
                  <span class="arrow"></span>
                  <a class="name" href="AboutNnb/Nnb.html" target="_blank;">企业信用信息公示系统动画教材</a>
              </li>
              <li>
                  <span class="arrow"></span>
                  <a class="name" href="ztxy.do?method=downLoadDoc&lx=1&random=189462371823">2013、2014年度企业年报须知</a>
              </li>
              <li class="color_f5f5f5">
                  <span class="arrow"></span>
                  <a class="name" href="ztxy.do?method=downLoadDoc&lx=2&random=189462371823">个体工商户年报须知</a>
              </li>
              <li>
                  <span class="arrow"></span>
                  <a class="name" href="ztxy.do?method=downLoadDoc&lx=3&random=1587239491123">个体工商户年度报告表（纸质版）</a>
              </li>
              <li>
                  <span class="arrow"></span>
                  <a class="name" href="ztxy.do?method=downLoadDoc&lx=5&random=1789345513431">企业工商信息联络员备案办事指南</a>
              </li>
              <li class="color_f5f5f5">
                  <span class="arrow"></span>
                  <a class="name" href="AboutNnb/AboutNnb.htm" target="_blank;">关于年报的那些事儿</a>
              </li>
          </ul>
     </div>
</div>
</div>
<style type="text/css">
.abc_upload_box a{color:#333;text-decoration:none;}
.abc_upload_box a:hover{text-decoration:underline;}
.abc_upload_box a{blr:expression(this.onFocus=this.close());}
.abc_upload_box a{blr:expression(this.onFocus=this.blur());}
.abc_upload_box a:focus{-moz-outline-style:none;}
.abc_upload_box a:focus{outline:none; }
.cl{clear:both;}
.fl{float:left;}

.abc_upload_box{
	width:400px;
	margin:0 auto;
	border:1px solid #dedede;
	background:#fff;
	overflow:hidden;
	font-size:12px;
	font-family:Tahoma, Geneva, sans-serif;
}

.abc_upload_title{
	width:100%;
	height:30px;
	line-height:32px;
	text-align:left;
	text-indent:40px;
	font-size:12px;
	font-weight:bold;
	color:#354368;
	background:#eef9ff url(framework/China/images/icon_upload_title.gif) 10px center no-repeat;
	border-bottom:1px solid #dedede;
	position:relative;
}

.abc_upload_title a{
	width:16px;
	height:16px;
	display:block;
	background:url(framework/China/images/icon_delete.gif) no-repeat;
	position:absolute;
	top:6px;
	right:10px;
}

.abc_upload_content{}

.abc_upload_content ul li{
	width:100%;
	height:40px;
}

.color_f5f5f5{background:#f5f5f5;}
.color_d4eeff{background:#d4eeff;}

.abc_upload_content ul li span.arrow{
	width:14px;
	height:14px;
	margin:13px 0 0 13px;
	background:url(framework/China/images/icon_arrow.png) left top no-repeat;
	display:block;
	float:left;
}

.abc_upload_content ul li a.name{
	width:300px;
	height:14px;
	margin:13px 0 0 13px;
	display:block;
	overflow:hidden;
	text-overflow:ellipsis;
	white-space:nowrap;
	float:left;
}

</style>
</div><br><br><br>
<div id="details" class="clear" >
	       <h2 style="margin-bottom: 15px;margin-top: 15px;">
	         利乐中国有限公司成都办事处&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;注册号/统一社会信用代码：企外川驻字第00070号 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				“该企业为吊销状态”
	       </h2>

  <div id="leftTabs" >
    <ul>
      	<li id="gs1" onclick="doPageDown('gs1')" class="current" style="margin-bottom:2px; "><div style="font-size: 18px;margin-top:55px;text-align: center;">工<br />商<br />公<br />示<br />信<br />息</div></li>


    </ul>
  </div>
  <!-- 工商公示信息 -->
  <div id="detailsCon_gs" >
    <div class="dConBox"  >
      <div class="tabs" id="tabs">
        <ul>
          <li id="0" class="current" onclick="doChange(this.id)">登记信息</li>
          <li id="5" onclick="doChange(this.id)">动产抵押登记信息</li>

          <li id="3" onclick="doChange(this.id)">行政处罚信息</li>
          <!-- xd.liu 2014-09-03 16:07 国家局0822文档要求调整顺序 -->
          <li id="6" onclick="doChange(this.id)">经营异常信息</li>

          <li id="7" onclick="doChange(this.id)">抽查检查信息</li>
        </ul>
      </div>
      <div id="jibenxinxi" >
</br>
<!-- 工商公示信息，登记信息 -->
<table cellspacing="0" cellpadding="0" class="detailsList" id="baseinfo">
      	<tr ><th colspan="4" style="text-align:center;">基本信息 </th></tr>
        <tr>
          <th width="20%">注册号/统一社会信用代码</th>
         <td width="30%">企外川驻字第00070号</td>
          <th>名称</th>
          <td width="30%">利乐中国有限公司成都办事处</td>
        </tr>
        <tr>
          <th>类型</th>
          <td>外国(地区)企业常驻代表机构</td>
          <th>派出企业名称</th>
          <td>利乐中国有限公司</td>
        </tr>
        <tr>
          <th width="20%">首席代表</th>
          <td>韦广彦</td>
          <th width="20%">成立日期</th>
          <td>1994年9月13日</td>
        </tr>
        <tr>
          <th>驻在场所</th>
          <td colspan="3">
           成都市西御街77号国信大厦7楼C座
			</td>
        	</tr>

        	<th >经营范围</th>
          <td colspan="3">本公司业务的咨询与联络。</td>
        </tr>
			<tr>
				<th>经营(驻在)期限自</th>
				<td></td>
				<th>经营(驻在)期限至</th>
				<td></td>
			</tr>
         <tr>
          <th>登记状态</th>
          <td> 		  	吊销，未注销
</td>
          <th >核准日期</th>
          <td>1999年8月10日</td>
        	</tr>
		  	<tr>
	          <th>吊销日期</th>
	          <td></td>
	          <th></th>
	          <td></td>
		  	</tr>
      </table>



<div id="biangeng" style="display:block;overflow:hidden">
				</br>
				<table  cellpadding="0" cellspacing="0" class="detailsList" id="table_bg">
					<tr width="95%"><th colspan="5" style="text-align:center;">变更信息</th></tr>
					<tr width="95%">
					<th width="20%" style="text-align:center;"> 变更事项</th>
					<th width="30%" style="text-align:center;"> 变更前内容</th>
					<th width="30%" style="text-align:center;"> 变更后内容</th>
					<th width="20%" style="text-align:center;"> 变更日期</th>
					</tr>
				</table><br/>
			</div>


 </div>

      <div id="beian" style="align:center;display:none">
         <br>
      </div>

     <!-- 工商公示信息，行政处罚 -->
    <div id="gsgsxx_xzcf" style="align:center;display:none">
         <br>
      </div>

      <div id="guquanchuzhi" style="display:none">
        </br>
      </div>
      <div id="dongchandiya" style="display:none">
      <br/>
      </div>
      <div id="yichangminglu" style="align:center;display:none">
        <div class="hh" style="text-align: center;">&nbsp;</div>
      </div>
      <div id="yanzhongweifa" style="align:center;display:none">
        <div class="hh" style="text-align: center;">&nbsp;</div>
      </div>
      <div id="chouchaxinxi" style="align:center;display:none">
         <div class="hh" style="text-align: center;">&nbsp;</div>
       </div>
      <div id="sipinyixie" style="align:center;display:none">
         <div class="hh" style="text-align: center;">&nbsp;</div>
       </div>
		<div id="jcxxfj" style="align:center;display:none">
		<br/>
		</div>
		<div id="yjxx" style="align:center;display:none">
		<br/>
		</div>
		<div id="jsxx" style="align:center;display:none">
		<br/>
		</div>
		<div id="tsxx" style="align:center;display:none">
		<br/>
		</div>
		<div id="xiaofeizhetousujubao" style="display:none;">
				<br>
		</div>
		<div id="jianyanjianche" style="display:none;">
				<br>
			</div>
    </div>
  </div>

  <!-- 企业公示信息 -->
  <div id="detailsCon_qy" style="display:none;">
    <div class="dConBox">
      <div class="tabs" id="qygsTabs">
        <ul>
        <li id="qygs_qynb" class="current" onclick="doPageRight(this.id);">
          <!-- xd.liu 2014-09-09 国家局0905文档要求修改文字 -->
            企业年报
        </li>


        </ul>

      </div>

      <div id="xzcf"  style="display:none">
      </div>
      <div id="qynb"  style="display:none">
      </div>
      <div id="tzrbgxx"  style="display:none">
      </div>
      <div id="xzxk"  style="display:none">
      </div>
      <div id="zzcq"  style="display:none">
      </div>
      <div id="tzrxx"  style="display:none">
      </div>

    </div>
  </div>


  <div id="detailsCon_qt" style="display:none;">
    <div class="dConBox">
      <div class="tabs" id="qtbmgsTabs">
        <ul>
        <li class="current" id="qtbm_xzxk" onclick="doPageLeft('xzxk');">行政许可信息</li>
        <li id="qtbm_xzcf" onclick="doPageLeft('xzcf');">行政处罚信息</li>
        </ul>

      </div>
      <div id="xingzhengxuke" style="display: none;">
        <br>
      </div>
      <div id="xingzhengchufa" style="display: none;">
        <br>
      </div>
      <div id="shengchananquanshigu" style="display: none;">
        <br>
      </div>

    </div>
  </div>

  <!-- xd.liu 2015-01-07 司法协助公示信息 -->
  <div id="detailsCon_sf" style="display:none;">
    <div class="dConBox">
      <div class="tabs" id="sfxzgsTabs">
        <ul>
        <li class="current" id="sfxz_gqdj" onclick="doPageLeftForGq('gqdj');">股权冻结信息</li>
        <li id="sfxz_gqbg" onclick="doPageLeftForGq('gqbg');">股东变更信息</li>
        </ul>

      </div>
      <div id="guquandongjie" style="display: none;">
        <br>
      </div>
      <div id="gudongbiangeng" style="display: none;">
        <br>
      </div>

    </div>
  </div>
  <!-- xd.liu 2015-02-09 其他公示信息 -->

  <div id="detailsCon_jb" style="display:none;">
    <div class="dConBox">
      <div class="tabs" id="xfztsjbTabs">
        <ul>
	  		<li class="current" id="xfztsjb"  onclick="doPageLeftOther('xfztsjb');">消费者投诉举报信息</li>
	  		<li class="current" id="jyjc"  onclick="doPageLeftOther('jyjc');">检验检测信息</li>
        </ul>
      </div>
    </div>
  </div>


</div>

</div>

<div style=" width:1010px; height:40px; margin:0px auto; color:#666; text-indent:0px; "><div class="banqun">

版权所有：四川省工商行政管理局　地址：成都市玉沙路118号　邮政编码：600017<br/>（为了更好的用户体验，建议您使用IE8或者以上版本浏览器） 　<a href="ztxy.do?method=downLoadDoc&lx=6&random=1789345513432" style="font-family:'微软雅黑';color:#fff">浏览器设置方法</a>
<div style="display: none;">
<script type="text/javascript">var cnzz_protocol = (("https:" == document.location.protocol) ? " https://" : " http://");document.write(unescape("%3Cspan id='cnzz_stat_icon_1000300163'%3E%3C/span%3E%3Cscript src='" + cnzz_protocol + "s5.cnzz.com/z_stat.php%3Fid%3D1000300163%26online%3D1%26show%3Dline' type='text/javascript'%3E%3C/script%3E"));</script>
</div>


</div>
</div>
</body>
</html>
<script>
function showRyxx(ryId,nbxh){
  var src="ztxy.do?method=tzrCzxxDetial&maent.xh="+ryId+"&maent.pripid="+nbxh+"&random="+new Date().getTime();
       _openPage(src);
}
function showMap(dom){
	var src="ztxy.do?method=showMap&dom="+dom+"&random="+new Date().getTime();
	_openPage(src);
}
</script>'''


enterprise_html_jingxi_zyry='''








<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>全国企业信用信息公示系统</title>
<link rel="stylesheet" type="text/css"
	href="http://gsxt.jxaic.gov.cn:80/ECPS//include/css/public3.css" />
<script type="text/javascript" src="/ECPS/include/js/jquery-1.9.0.min.js"></script>
<script type="text/javascript">
$(function(){
		var h = $("#main").height();
		if(!window.parent.document.getElementById('detailsCon4')){
			if(h < 780){
				h = 780;
			}
		}else{
			if(h < 970){
				h = 970;
			}
		}
		$("#detailsCon1",window.parent.document).css("height",h+50);
		$("#gsgsIframe",window.parent.document).css("height",h+20);
})
</script>
</head>

<body>
<div id="main">

	<br>
	<table style="width:100%; id=" t30" cellpadding="0" cellspacing="0"
		class="detailsList">
		<tr width="939px">
			<th colspan="6" style="text-align:center;">
				主要人员信息
			</th>
		</tr>
		<th style="width:10%;text-align:center">序号</th>
		<th style="width:20%;text-align:center">姓名</th>
		<th style="width:20%;text-align:center">职务</th>
		<th style="width:10%;text-align:center">序号</th>
		<th style="width:20%;text-align:center">姓名</th>
		<th style="width:20%;text-align:center">职务</th>
		</tr>



				<tr>
					<td style="text-align:center;">1</td>
					<td>曾敏</td>
					<td>监事</td>
					<td style="text-align:center;">2</td>
					<td>苏友明</td>
					<td>执行董事兼总经理</td>
				</tr>





	</table>
	<br>

	<table id="t31" cellpadding="0" cellspacing="0" class="detailsList">
		<tr width="939px">
			<th colspan="4" style="text-align:center;">分支机构信息</th>
		</tr>
		<tr>
			<th style="text-align:center;width:10%;">序号</th>
			<th style="text-align:center;width:25%">注册号/统一社会信用代码</th>
			<th style="text-align:center;width:25%">名称</th>
			<th style="text-align:center;width:20%">登记机关</th>
		</tr>

	</table>
	<br>

	<table id="t32" cellpadding="0" cellspacing="0" class="detailsList">
		<tr width="939px">
			<th colspan="4" style="text-align:center;">清算信息</th>
		</tr>
		<tr>
			<th style="width:20%">清算负责人</th>
			<td style="width:80%">

			</td>
		</tr>
		<tr>
			<th style="width:20%">清算组成员</th>
			<td style="width:80%">

			</td>
		</tr>

	</table>

</div>
</body>
</html>'''


enterprise_html_guangdong_szxy = '''

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>
	市场主体信用信息公示系统
</title><link href="css/public3.css" type="text/css" rel="stylesheet" />
    <script type="text/javascript">
        function r0() {
            document.getElementById('jibenxinxi').style.display = 'block';
            document.getElementById('biangengxinxi').style.display = 'block';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('guquanchuzi').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('jingyingyichang').style.display = 'none';
            document.getElementById('yanzhongweifa').style.display = 'none';
            document.getElementById('chouchajiancha').style.display = 'none';
        }
        function r1() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('biangengxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'block';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('guquanchuzi').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('jingyingyichang').style.display = 'none';
            document.getElementById('yanzhongweifa').style.display = 'none';
            document.getElementById('chouchajiancha').style.display = 'none';
        }
        function r2() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('biangengxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'block';
            document.getElementById('guquanchuzi').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('jingyingyichang').style.display = 'none';
            document.getElementById('yanzhongweifa').style.display = 'none';
            document.getElementById('chouchajiancha').style.display = 'none';
        }
        function r3() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('biangengxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('guquanchuzi').style.display = 'block';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('jingyingyichang').style.display = 'none';
            document.getElementById('yanzhongweifa').style.display = 'none';
            document.getElementById('chouchajiancha').style.display = 'none';
        }
        function r4() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('biangengxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('guquanchuzi').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'block';
            document.getElementById('jingyingyichang').style.display = 'none';
            document.getElementById('yanzhongweifa').style.display = 'none';
            document.getElementById('chouchajiancha').style.display = 'none';
        }
        function r5() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('biangengxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('guquanchuzi').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('jingyingyichang').style.display = 'block';
            document.getElementById('yanzhongweifa').style.display = 'none';
            document.getElementById('chouchajiancha').style.display = 'none';
        }
        function r6() {
            document.getElementById('jibenxinxi').style.display = 'none';;
            document.getElementById('biangengxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('guquanchuzi').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('jingyingyichang').style.display = 'none';
            document.getElementById('yanzhongweifa').style.display = 'block';
            document.getElementById('chouchajiancha').style.display = 'none';
        }
        function r7() {
            document.getElementById('jibenxinxi').style.display = 'none';
            document.getElementById('biangengxinxi').style.display = 'none';
            document.getElementById('beian').style.display = 'none';
            document.getElementById('dongchandiya').style.display = 'none';
            document.getElementById('guquanchuzi').style.display = 'none';
            document.getElementById('xingzhengchufa').style.display = 'none';
            document.getElementById('jingyingyichang').style.display = 'none';
            document.getElementById('yanzhongweifa').style.display = 'none';
            document.getElementById('chouchajiancha').style.display = 'block';
        }

        function togo(str) {
            var Request = new Object();
            Request = GetRequest();
            if (str == '1') {
                window.location = 'QyxyDetail.aspx?rid=' + Request['rid'];
            } else if (str == '2') {
                window.location = 'QynbDetail.aspx?rid=' + Request['rid'];
            } else if (str == '3') {
                window.location = 'QtbmDetail.aspx?rid=' + Request['rid'];
            }
        }

        function GetRequest() {
            var url = location.search; //获取url中"?"符后的字串
            var theRequest = new Object();
            if (url.indexOf("?") != -1) {
                var str = url.substr(1);
                strs = str.split("&");
                for (var i = 0; i < strs.length; i++) {
                    theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
                }
            }
            return theRequest;
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

                }
                else {
                    liAry[i].className = "";
                }
            }
        }

        function ShowSpan(obj, n) {
            var span = obj.parentNode.getElementsByTagName("tabs");
            for (var i = 0; i < span.length; i++) {
                span[i].className = "current";
            }
            span[n].className = "";
            var li = obj.parentNode.getElementsByTagName("li")
            li[n].className = "current";
            for (var i = 0; i < li.length; i++) {
                if (i != n) {
                    li[i].className = "";
                }
                li[i].onmouseout = function () {
                    this.className = "current";
                }
            }
        }
    </script>
</head>
<body>
    <form method="post" action="./QyxyDetail.aspx?rid=a124285cae2d403d9c066fb65b83976c" id="form1">
<div class="aspNetHidden">
<input type="hidden" name="__EVENTTARGET" id="__EVENTTARGET" value="" />
<input type="hidden" name="__EVENTARGUMENT" id="__EVENTARGUMENT" value="" />
<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="/wEPDwUJNTAwNTM1MDYyD2QWAgIDD2QWDAIDD2QWAmYPZBYEAgEPDxYCHgRUZXh0Be4BIDxoMiBpZD0iZ3NoMiI+5rex5Zyz5biC5Lqa5YWL5Zac5aSa5pav55S15a2Q56eR5oqA5pyJ6ZmQ5YWs5Y+4ICZuYnNwOyZuYnNwOyAmbmJzcDsmbmJzcDsmbmJzcDsmbmJzcDsgJm5ic3A7Jm5ic3A75rOo5YaM5Y+377yaNDQwMzAxMTA2MDkwNjUyJm5ic3A7Jm5ic3A7ICZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOyAmbmJzcDsmbmJzcDvigJzor6XkvIHkuJrlt7LliJflhaXnu4/okKXlvILluLjlkI3lvZXigJ08L2gyPmRkAgMPZBYEZg9kFhgCAw8PFgIfAAUPNDQwMzAxMTA2MDkwNjUyZGQCBQ8PFgIfAAUw5rex5Zyz5biC5Lqa5YWL5Zac5aSa5pav55S15a2Q56eR5oqA5pyJ6ZmQ5YWs5Y+4ZGQCBw8PFgIfAAUn5pyJ6ZmQ6LSj5Lu75YWs5Y+477yI6Ieq54S25Lq654us6LWE77yJZGQCCQ8PFgIfAAUe6Zi/5Y2c5p2c54Ot5ZCI5pu877yO57Gz5ZCJ5o+QZGQCCw8PFgIfAAUSMTAw5LiH5YWD5Lq65rCR5biBZGQCDQ8PFgIfAAURMjAxMuW5tDAz5pyIMjLml6VkZAIPDw8WAh8ABSvmt7HlnLPluILnpo/nlLDljLrljY7lvLrljJfotZvmoLzlub/lnLozNjExZGQCEQ8PFgIfAAURMjAxMuW5tDAz5pyIMjLml6VkZAITDw8WAh8ABREyMDIy5bm0MDPmnIgyMuaXpWRkAhUPDxYCHwAFJ+a3seWcs+W4guW4guWcuuebkeedo+euoeeQhuWxgOemj+eUsOWxgGRkAhcPDxYCHwAFETIwMTPlubQwOeaciDI25pelZGQCGQ8PFgIfAAUM55m76K6w5oiQ56uLZGQCAQ9kFgICAQ8WAh4LXyFJdGVtQ291bnQCARYCZg9kFgJmDxUECeiHqueEtuS6uh7pmL/ljZzmnZzng63lkIjmm7zvvI7nsbPlkInmj5AAIGYzMzZkNDI0MGNlZTRmMDdhZWMyMTIwZjk4OGY2MmE2ZAIHD2QWBgIBD2QWAgIBD2QWAgIBD2QWAgIBDw8WAh8ABbsB5omL5py644CB5omL5py655S15rGg44CB5pWw56CB5Lqn5ZOB44CB56e75Yqo55S15rqQ44CB5pWw56CB5Lqn5ZOB55S15rGg44CB55S15a2Q5Lqn5ZOB44CB6K6h566X5py66L2v5Lu25Y+K56Gs5Lu26K6+5aSH55qE5oqA5pyv5byA5Y+R5LiO6ZSA5ZSu77yb5Zu95YaF6LS45piT77yb57uP6JCl6L+b5Ye65Y+j5Lia5Yqh44CCXmRkAgIPZBYCAgEPFgIfAAWyAjx0cj48dGQgc3R5bGU9InRleHQtYWxpZ246Y2VudGVyOyI+MTwvdGQ+PHRkPuiJvum6puWwlO+8juiJvuWQiOm6puaPkDwvdGQ+PHRkPuebkeS6izwvdGQ+PHRkIHN0eWxlPSJ0ZXh0LWFsaWduOmNlbnRlcjsiPjI8L3RkPjx0ZD7pmL/ljZzmnZzng63lkIjmm7zvvI7nsbPlkInmj5A8L3RkPjx0ZD7miafooYzvvIjluLjliqHvvInokaPkuos8L3RkPjwvdHI+PHRyPjx0ZCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij4zPC90ZD48dGQ+6Zi/5Y2c5p2c54Ot5ZCI5pu877yO57Gz5ZCJ5o+QPC90ZD48dGQ+5oC757uP55CGPC90ZD48L3RyPmQCBA9kFgQCAQ8WAh4HVmlzaWJsZWhkAgMPFgIfAmhkAgkPZBYCAgEPZBYCAgMPFgIfAmdkAgsPZBYCAgEPZBYCAgMPFgIfAmdkAg8PZBYCAgEPZBYCAgEPFgIfAQICFgRmD2QWAmYPFQYBMTbpgJrov4fnmbvorrDnmoTkvY/miYDmiJbnu4/okKXlnLrmiYDml6Dms5Xlj5blvpfogZTns7sRMjAxNOW5tDA25pyIMDnml6UAABvnpo/nlLDluILlnLrnm5HnnaPnrqHnkIblsYBkAgEPZBYCZg8VBgEyH+acquaMieaXtuaPkOS6pDIwMTTlubTluqbmiqXlkYoRMjAxNeW5tDA45pyIMjTml6UAABvnpo/nlLDluILlnLrnm5HnnaPnrqHnkIblsYBkAhMPZBYCAgEPZBYCAgMPFgIfAmdkZPcl1MT8i3UlYpWdcdmC/KTVE/Cl" />
</div>

<script type="text/javascript">
//<![CDATA[
var theForm = document.forms['form1'];
if (!theForm) {
    theForm = document.form1;
}
function __doPostBack(eventTarget, eventArgument) {
    if (!theForm.onsubmit || (theForm.onsubmit() != false)) {
        theForm.__EVENTTARGET.value = eventTarget;
        theForm.__EVENTARGUMENT.value = eventArgument;
        theForm.submit();
    }
}
//]]>
</script>


<script src="/web/WebResource.axd?d=5d5KGRMAyLvBqg6D0Z6Xhj3Bik0iH8Qt5h7ZqLwbqRWMcG_QNGx9uHHYTzhIEQhPxWH_P8u88WPt72kX0&amp;t=635802961220000000" type="text/javascript"></script>


<script src="/web/ScriptResource.axd?d=a8XuVJe3RPmNNezBCV4fnhmFCTQPZUJuIVB1PICLRIFB0h0iFOT51is_Q9pzVzBg5YWBLBKS1CWtbSPylPaRTjWmvnSuN_4Vp_BgSDtPqcL64afEn05pWbSSNySR9Mydpi-0VtLHKkLXQpp5CBE1Sm7fImxVdYLGKHFTJg2&amp;t=5f9d5645" type="text/javascript"></script>
<script type="text/javascript">
//<![CDATA[
if (typeof(Sys) === 'undefined') throw new Error('ASP.NET Ajax 客户端框架未能加载。');
//]]>
</script>

<script src="/web/ScriptResource.axd?d=_qZPvnuQ-IwWQrnKXhnIvLRxioe9O-Ab28fk3EAfgQLrvQZtwHiPgSDxbsHi67wW8f6eI0EuCp8CTlwgUL3vc2j57a0O3cWaN1_EDEf2zcEG9MkETRna5PCL5Le_ddeJuIRt7UWsXRMwb7i8yeDTW26c9B0FuBPQG3y93LM-E-2H2qGe0&amp;t=5f9d5645" type="text/javascript"></script>
<script src="/web/ScriptResource.axd?d=7GuTBO4rPX36CPWWCNLwicjZWD3CM8OiqEFMz3LjfUh2zFhXeO6-xGEA79_e14ujC2yvLHWhGMSXyPm0CYyndKmRJLUwVdfLKN8hUbPo2bFk3AtC_iI8E414pv-WaKtPiO3qiv1dfYlTE6K9SSAZbs11IhEnS9XJilUb-w2&amp;t=5f9d5645" type="text/javascript"></script>
<div class="aspNetHidden">

	<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="1ED7F22A" />
</div>
    <script type="text/javascript">
//<![CDATA[
Sys.WebForms.PageRequestManager._initialize('ScriptManager1', 'form1', ['tUpdatePanel1','UpdatePanel1','tbiangengxinxi','biangengxinxi','txingzhengchufa','xingzhengchufa'], [], [], 90, '');
//]]>
</script>

    <div id="header">
	<div class="top">
		<div class="top-a">
			<a href="http://gsxt.gdgs.gov.cn/">全国首页</a>
			<a href="http://gsxt.saic.gov.cn">地方局首页</a>
		 </div>
	</div>
</div><br><br><br><br>


    <div id="details" class="clear">
    <div id="UpdatePanel1">

        <span id="EntName" style="font-family:幼圆;font-size:18pt;font-weight:bold;"> <h2 id="gsh2">深圳市亚克喜多斯电子科技有限公司 &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;注册号：440301106090652&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;“该企业已列入经营异常名录”</h2></span>
        <div id="infoPanel">

  <div id="leftTabs" >
    <ul>
      <li class="current" style="margin-bottom:2px;"><p>工<br />商<br />公<br />示<br />信<br />息</p></li>
      <li onclick="togo('2')" style="margin-bottom:2px;"><p>企<br />业<br />公<br />示<br />信<br />息</p></li>
      <li onclick="togo('3')" style="margin-bottom:2px;"><p>其<br />他<br />部<br />门<br />公<br />示<br />信<br />息</p></li>
    </ul>
  </div>
  <div id="detailsCon" style="height:800px;overflow:auto;overflow-x: hidden;">
    <div class="dConBox"  >
<div class="tabs" id="tabs">
        <ul>

        <li id="0" class="current" onclick="r0(),changeStyle('tabs',this)">登记信息</li>
					<li id="1" onclick="r1(),changeStyle('tabs',this)">备案信息</li>
					<li id="2" onclick="r2(),changeStyle('tabs',this)">动产抵押登记信息</li>
					<li id="3" onclick="r3(),changeStyle('tabs',this)">股权出质登记信息</li>
					<li id="4" onclick="r4(),changeStyle('tabs',this)">行政处罚信息</li>
					<li id="5" onclick="r5(),changeStyle('tabs',this)">经营异常信息</li>
					<li id="6" onclick="r6(),changeStyle('tabs',this)">严重违法信息</li>
					<li id="7" onclick="r7(),changeStyle('tabs',this)">抽查检查信息</li>
        </ul>
      </div>
       <div id="jibenxinxi">
       <br />
      <table cellspacing="0" cellpadding="0" class="detailsList" >
      	<tr><th colspan="4" style="text-align:center;">基本信息 </th></tr>
        <tr>
          <th width="20%">统一社会信用代码</th>
         <td width="30%" colspan="3"><span id="infoUC_RegInfo_SSDJYXZRGS_EntSCCode"></span></td>
        </tr>
        <tr>
          <th width="20%">注册号</th>
         <td width="30%"><span id="infoUC_RegInfo_SSDJYXZRGS_EntRegNO">440301106090652</span></td>
          <th>名称</th>
          <td width="30%"><span id="infoUC_RegInfo_SSDJYXZRGS_EntName1">深圳市亚克喜多斯电子科技有限公司</span></td>
        </tr>
        <tr>
          <th>类型</th>
        <td><span id="infoUC_RegInfo_SSDJYXZRGS_EntTypeCode1">有限责任公司（自然人独资）</span></td>
          <th width="20%">法定代表人</th>
           <td><span id="infoUC_RegInfo_SSDJYXZRGS_Name1">阿卜杜热合曼．米吉提</span></td>
		</tr>
        <tr>
           <th>注册资本</th>
          <td><span id="infoUC_RegInfo_SSDJYXZRGS_RegCap1">100万元人民币</span></td>
		  <th width="20%">成立日期</th>
          <td><span id="infoUC_RegInfo_SSDJYXZRGS_EstDate1">2012年03月22日</span></td>

        </tr>
        <tr>
          <th>住所</th>
           <td colspan="3"><span id="infoUC_RegInfo_SSDJYXZRGS_Addr1">深圳市福田区华强北赛格广场3611</span></td>
        </tr>
        <tr>
        	<th>营业期限自</th>
            <td><span id="infoUC_RegInfo_SSDJYXZRGS_OpFromDate1">2012年03月22日</span></td>
          <th>营业期限至</th>
          <td><span id="infoUC_RegInfo_SSDJYXZRGS_OpToDate1">2022年03月22日</span></td>
        </tr>

		  <tr>
        	<th>登记机关</th>
            <td><span id="infoUC_RegInfo_SSDJYXZRGS_DeptName1">深圳市市场监督管理局福田局</span></td>
          <th>核准日期</th>
          <td><span id="infoUC_RegInfo_SSDJYXZRGS_AuthDate1">2013年09月26日</span></td>
        </tr>
         <tr>
        	<th>经营状态</th>
          <td><span id="infoUC_RegInfo_SSDJYXZRGS_EntStatusCode1">登记成立</span></td>
          <th></th>
          <td></td>
        </tr>
        </table>
<br />
<table cellspacing="0" cellpadding="0" class="detailsList"  id="Table1" >
<tr><th colspan="5" style="text-align:center;">投资人信息 </th></tr>
<tbody id="table2">
       <tr width="95%">
       	<th width="10%" style="text-align:center;">投资人类型</th>
          <th width="10%" style="text-align:center;">投资人</th>
		  <th width="10%" style="text-align:center;">证照类型</th>
		  <th width="10%" style="text-align:center;">证照号码</th>
		  <th width="10%" style="text-align:center;">详情</th>
        </tr>

    <tr>
        <td>自然人</td>
        <td>阿卜杜热合曼．米吉提</td>
	    <td></td>
        <td></td>
	    <td><a href='EntSHDetail.aspx?rid=f336d4240cee4f07aec2120f988f62a6' target="_blank">查看详情</a> </td>
    </tr>

</tbody>
</table>
<br />
	</div>

</div>
  <div id="biangengxinxi">

  <span id="Timer2" style="visibility:hidden;display:none;"></span>
  <div>
        <div id="alterPanel">


	</div>
    </div>

</div>
  <div id="beian" style="align: center; display: none; overflow: auto;
        overflow-x: hidden;">
        <div id="beianPanel">


<br />
<table id="t32" cellpadding="0" cellspacing="0" class="detailsList">
    <tr width="939px">
        <th colspan="5" style="text-align: center;">
            经营范围信息
        </th>
    </tr>
    <tr id="RegInfo_SSDJCBuItem_tr1">
		<th style="width: 20%">
            章程记载的经营范围
        </th>
		<td colspan="4">
            <span id="RegInfo_SSDJCBuItem_labCBuItem">手机、手机电池、数码产品、移动电源、数码产品电池、电子产品、计算机软件及硬件设备的技术开发与销售；国内贸易；经营进出口业务。^</span>
        </td>
	</tr>

</table>


<br />
<table style="width: 100%;" id="t30" cellpadding="0" cellspacing="0" class="detailsList">
    <tr width="939px">
        <th colspan="6" style="text-align: center;">
            主要人员信息
        </th>
    </tr>
    <th style="width: 10%; text-align: center">
        序号
    </th>
    <th style="width: 20%; text-align: center">
        姓名
    </th>
    <th style="width: 20%; text-align: center">
        职务
    </th>
    <th style="width: 10%; text-align: center">
        序号
    </th>
    <th style="width: 20%; text-align: center">
        姓名
    </th>
    <th style="width: 20%; text-align: center">
        职务
    </th>
    </tr>
    <tr><td style="text-align:center;">1</td><td>艾麦尔．艾合麦提</td><td>监事</td><td style="text-align:center;">2</td><td>阿卜杜热合曼．米吉提</td><td>执行（常务）董事</td></tr><tr><td style="text-align:center;">3</td><td>阿卜杜热合曼．米吉提</td><td>总经理</td></tr>
</table>

<br />
<table id="t31"   cellpadding="0" cellspacing="0" class="detailsList"  >
					<tr width="939px">
					<th colspan="4" style="text-align:center;">分支机构信息</th>
				</tr>
				<tr>
					  <th style="text-align:center;width:10%;">序号</th>
					  <th style="text-align:center;width:25%">注册号</th>
					  <th style="text-align:center;width:25%">名称</th>
					  <th style="text-align:center;width:20%">登记机关</th>
					 </tr>


				</tr>
				</table>
<br />
<table id="t32" cellpadding="0" cellspacing="0" class="detailsList">
    <tr width="939px">
        <th colspan="5" style="text-align: center;">
            清算信息
        </th>
    </tr>



</table>

</div>
    </div><br />
    <div id="dongchandiya" style="align: center; display: none; height: 850px; overflow: auto;
        overflow-x: hidden;">
        <div id="dongchandiyaPanel">


<table  cellpadding="0" cellspacing="0" class="detailsList">
					<tr width="95%"><th colspan="9" style="text-align:center;">动产抵押登记信息</th></tr>
					<tr width="95%">

                    <th width="5%" style="text-align:center;">序号</th>
						<th width="25%" style="text-align:center;">登记编号</th>
						<th width="15%" style="text-align:center;">登记日期</th>
						<th width="20%" style="text-align:center;">登记机关</th>
						<th width="15%" style="text-align:center;">被担保债权数额</th>
						<th width="10%" style="text-align:center;">状态</th>
						<th width="10%" style="text-align:center;">详情</th>

					</tr>

				<tr id="RegInfo_DCDYInfo_trNoInfo" width="95%">
		<td colspan="9" style="text-align:center;">暂无动产抵押登记信息。</td>
	</tr>


				</table><br/>
</div>
        <br />
    </div>
    <div id="guquanchuzi" style="align: center; display: none; height: 850px; overflow: auto;
        overflow-x: hidden;">
        <div id="GQCZPanel">


<table  cellpadding="0" cellspacing="0" class="detailsList">
							<tr width="95%"><th colspan="10" style="text-align:center;">股权出质登记信息</th></tr>
          <tr width="95%">
						<th width="5%"style="text-align:center;">序号</th>
						<th width="10%"style="text-align:center;">登记编号</th>
						<th width="10%"style="text-align:center;">出质人</th>
						<th width="12%"style="text-align:center;">证照/证件号码</th>
						<th width="10%"style="text-align:center;">出质股权数额</th>
						<th width="10%"style="text-align:center;">质权人</th>
						<th width="12%"style="text-align:center;">证照/证件号码</th>
						<th width="15%"style="text-align:center;">股权出质设立登记日期</th>
						<th width="8%"style="text-align:center;">状态</th>
						<th width="8%"style="text-align:center;">详情</th>



                </tr>

					<tr id="RegInfo_GQZYInfo_trNoInfo" width="95%">
		<td colspan="9" style="text-align:center;">暂无股权出质登记信息。</td>
	</tr>

					<tr>
					<th colspan="10" style="text-align:rigth;"><a><<</a>&nbsp;&nbsp;<a>1</a>&nbsp;&nbsp;<a>>></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
					</tr>
				</table><br />
</div>
        <br />
    </div>
  <div id="xingzhengchufa" style="align: center; display: none; height: 850px; overflow: auto;
        overflow-x: hidden;">

  <span id="Timer1" style="visibility:hidden;display:none;"></span>
    <div>
        <div id="XZCFPanel">


	</div>
    </div>

</div>
    <div id="jingyingyichang" style="align: center; display: none; height:850px; overflow: auto;
        overflow-x: hidden;">
        <div id="JYYCPanel">


<table  cellpadding="0" cellspacing="0" class="detailsList">
					<tr width="95%"><th colspan="9" style="text-align:center;">异常名录信息</th></tr>
					<tr width="95%">
					<th width="5%"style="text-align:center;">序号</th>
						<th width="25%"style="text-align:center;">列入经营异常名录原因</th>
						<th width="10%"style="text-align:center;">列入日期</th>
						<th width="27%"style="text-align:center;">移出经营异常名录原因</th>
						<th width="10%"style="text-align:center;">移出日期</th>
						<th width="10%"style="text-align:center;">作出决定机关</th>
					</tr>


				<tr width="95%">
				<td style="text-align:center;width:5%;">1</td>
				<td style="text-align:center;">通过登记的住所或经营场所无法取得联系</td>
                <td style="text-align:center;">2014年06月09日</td>
				<td style="text-align:center;"></td>
				<td style="text-align:center;"></td>
				<td style="text-align:center;">福田市场监督管理局</td>
				</tr>


				<tr width="95%">
				<td style="text-align:center;width:5%;">2</td>
				<td style="text-align:center;">未按时提交2014年度报告</td>
                <td style="text-align:center;">2015年08月24日</td>
				<td style="text-align:center;"></td>
				<td style="text-align:center;"></td>
				<td style="text-align:center;">福田市场监督管理局</td>
				</tr>




                    <tr>
				 <th colspan="6" style="text-align:rigth;"><a><<</a>&nbsp;&nbsp;<a>1</a>&nbsp;&nbsp;<a>>></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
				</tr>
				</table><br/>
</div>
    </div>
    <div id="yanzhongweifa" style="align: center; display: none; height: 850px; overflow: auto;
        overflow-x: hidden;">
        <div id="YZWFPanel">


<table  cellpadding="0" cellspacing="0" class="detailsList">
							<tr width="95%"><th colspan="6" style="text-align:center;">严重违法信息</th></tr>
					<tr width="95%">
						<th width="5%"style="text-align:center;">序号</th>
						<th width="25%"style="text-align:center;">列入严重违法企业名单原因</th>
						<th width="13%"style="text-align:center;">列入日期</th>
						<th width="20%"style="text-align:center;">移出严重违法企业名单原因</th>
						<th width="13%"style="text-align:center;">移出日期</th>
						<th width="24%"style="text-align:center;">作出决定机关</th>
					</tr>
                    <tr width="95%">
				 <td width="888px" colspan="6" style="text-align:center;">
				  	暂无严重违法信息
				  </td>
					</tr>
				<tr>
				 <th colspan="6" style="text-align:rigth;"><a><<</a>&nbsp;&nbsp;<a>1</a>&nbsp;&nbsp;<a>>></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
				</tr>
				</table><br/>
</div>
        <br />
    </div>
     <div id="chouchajiancha" style="align: center; display: none; height: 850px; overflow: auto;
        overflow-x: hidden;">
        <div id="CCJCPanel">


<table  cellpadding="0" cellspacing="0" class="detailsList">
							<tr><th colspan="6" style="text-align:center;">抽查检查信息</th></tr>
				<tbody id="tableChoucha">
					<tr>
						<th width="5%"style="text-align:center;">序号</th>
						<th width="25%"style="text-align:center;">检查实施机关</th>
						<th width="10%"style="text-align:center;">类型</th>
						<th width="15%"style="text-align:center;">日期</th>
						<th width="25%"style="text-align:center;">结果</th>
                        <th width="20%"style="text-align:center;">备注</th>
					</tr>

				<tr id="RegInfo_CCJCInfo_trNoInfo" width="95%">
		<td colspan="6" style="text-align:center;">暂无抽查检查信息。</td>
	</tr>


                    <tr>
				 <th colspan="6" style="text-align:rigth;"><a><<</a>&nbsp;&nbsp;<a>1</a>&nbsp;&nbsp;<a>>></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
				</tr>
                </tbody>
				</table><br/>
</div>
    </div>
    </div>



    <div id="footer">
        <img src="images/footer.gif" width="990" /></div>


<script type="text/javascript">
//<![CDATA[
Sys.Application.add_init(function() {
    $create(Sys.UI._Timer, {"enabled":true,"interval":100,"uniqueID":"Timer2"}, null, null, $get("Timer2"));
});
Sys.Application.add_init(function() {
    $create(Sys.UI._Timer, {"enabled":true,"interval":20,"uniqueID":"Timer1"}, null, null, $get("Timer1"));
});
//]]>
</script>
</form>
</body>
</html>
'''

enterprise_html_jiangxi_jbxx = '''







<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>全国企业信用信息公示系统</title>
	<link rel="stylesheet" type="text/css" href="http://gsxt.jxaic.gov.cn:80/ECPS//include/css/public3.css" />
	<link rel="stylesheet" type="text/css" href="http://gsxt.jxaic.gov.cn:80/ECPS//include/css/style.css"/>
	<link rel="stylesheet" type="text/css" href="http://gsxt.jxaic.gov.cn:80/ECPS//include/js/page/pageGroup.css"/>
	<script type="text/javascript" src="/ECPS/include/js/jquery-1.9.0.min.js"></script>
	<script type="text/javascript" src="http://gsxt.jxaic.gov.cn:80/ECPS//include/js/page/jquery-1.8.3.min.js"></script>
	<script type="text/javascript" src="http://gsxt.jxaic.gov.cn:80/ECPS//include/js/page/pageGroup.js"></script>
	<script type="text/javascript" src="/ECPS/include/js/pager.js"></script>
<script type="text/javascript">
$(function(){
		var h = $("#main").height();
		$("#gdxxf",window.parent.document).css("height",h);
		$("#gdxxIframe",window.parent.document).css("height",h);
})
</script>
</head>
<body>
<div id="main">
	<br/>
	<form action="/ECPS/ccjcgs/gsgs_viewDjxxGdxx.pt?qyid=3600006000050563" method="post">
	<table id="table3" cellspacing="0" cellpadding="0" class="detailsList" >
		<tr>
			<th colspan="5" style="text-align:center;">


					股东信息
				<br>
				<h1 style="text-align:center;">股东的出资信息截止2014年2月28日。2014年2月28日之后工商只公示股东姓名，其他出资信息由企业自行公示。</h1>
			</th>
		</tr>
		<tbody id="table3">
			<tr width="95%">
				<th width="20%" style="text-align:center;">


					股东类型


				</th>
				<th width="20%" style="text-align:center;">


					股东

				</th>
				<th width="20%" style="text-align:center;">证照/证件类型</th>
				<th width="20%" style="text-align:center;">证照/证件号码</th>


					股东

				</th>

					<th width="20%" style="text-align:center;">详情</th>

			</tr>


				<tr>
					<td>外商投资企业</td>
					<td>江西铜业股份有限公司</td>
					<td>企业法人营业执照(公司)

					</td>
					<td>
						360000521000033

					</td>

						<td>

						</td>

				</tr>



			<tr>
				<th colspan="5">
					<script type="text/javascript">
						getPager2('1','1','1','5');
				  	</script>
				  	<input type="hidden" id="totalPage" value="1" />
				  	<input type="hidden" id="pageNum" value="1" />
				  	<input type="hidden" id="mark" name="mark" value="" />
				</th>
			</tr>

		</tbody>
	</table>

</form>
</div>
</body>
</html>'''

enterprise_html_beijing_bgxx = '''




<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet" />
	<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script><!-- 1.9版本jQuery js   -->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/pubInfo.js"></script><!-- 北京首页pubInfo.js js   -->
	<script type="text/javascript" src="/js/ajax/http.js" ></script>
	<script type="text/javascript">
	var rootPath = '';
 	var entId = '14574FC50AA04CACA67E020E20B98680';
	var entName = '北京暴风科技股份有限公司';
	var entNo = '';
	</script>
	<style>
	html { overflow:hidden; }
	</style>
</head>
<body>
	<form action="gjjbj/gjjQueryCreditAction!biangengFrame.dhtml" method="post"  name="iframeFrame" id="iframeFrame">
	<input type="hidden" id="pageNos" name="pageNos" value="1" />
	<input type="hidden" id="ent_id" name="ent_id" value="14574FC50AA04CACA67E020E20B98680"/>
	<table cellspacing="0" cellpadding="0" class="detailsList"  id="touziren" >
		<tbody id="table2">
			<tr width="95%"><th colspan="4" style="text-align:center;">变更信息</th></tr>
			<tr width="95%">
			<th width="15%" style="text-align:center;"> 变更事项</th>
			<th width="25%" style="text-align:center;"> 变更前内容</th>
			<th width="25%" style="text-align:center;"> 变更后内容</th>
			<th width="10%" style="text-align:center;"> 变更日期</th>
			</tr>



	         <tr id="tr1">
	         	<td>董事（理事）、经理、监事</td>

		         	<td colspan='2'><a href="javascript:void(0);" onclick="showDialog('/gjjbj/gjjQueryCreditAction!zyryBgxx.dhtml?old_reg_his_id=20e38b8c511f4011015123d40b6d1253&new_reg_his_id=ff808081531d0fa601533649316c1b38&clear=true&chr_id=null', '投资人信息详细', '468px');">详细</a></td>

	         	<td>2016-03-02</td>
	         </tr>

	         <tr id="tr1">
	         	<td>注册资本</td>

	         		<td>12000万元</td>
		         	<td>27385.7085万元</td>


	         	<td>2015-11-20</td>
	         </tr>

	         <tr id="tr1">
	         	<td>董事（理事）、经理、监事</td>

		         	<td colspan='2'><a href="javascript:void(0);" onclick="showDialog('/gjjbj/gjjQueryCreditAction!zyryBgxx.dhtml?old_reg_his_id=20e38b8b4029e2b2014052c4cac82218&new_reg_his_id=20e38b8c511f4011015123d40b6d1253&clear=true&chr_id=null', '投资人信息详细', '468px');">详细</a></td>

	         	<td>2015-11-20</td>
	         </tr>

	         <tr id="tr1">
	         	<td>经营范围</td>

	         		<td>互联网信息服务业务（除新闻、教育、医疗保健、医疗器械以外的内容）（电信与信息服务业务经营许可证有效期至2017年6月18日）。技术开发、技术服务、技术转让、技术咨询；计算机系统集成；设计、制作、代理、发布广告；组织文化艺术交流活动（演出除外）；销售电子产品、计算机、软硬件及辅助设备。依法须经批准的项目，经相关部门批准后依批准的内容开展经营活动。</td>
		         	<td>互联网信息服务业务（除新闻、教育、医疗保健、医疗器械以外的内容）（电信与信息服务业务经营许可证有效期至2017年6月18日）。技术开发、技术服务、技术转让、技术咨询；计算机系统集成；设计、制作、代理、发布广告；组织文化艺术交流活动（演出除外）；销售电子产品、计算机、软硬件及辅助设备；演出经纪业务；文艺创作。演出经纪以及依法须经批准的项目，经相关部门批准后依批准的内容开展经营活动。</td>


	         	<td>2015-09-07</td>
	         </tr>

	         <tr id="tr1">
	         	<td>注册资本</td>

	         		<td>9000万元</td>
		         	<td>12000万元</td>


	         	<td>2015-07-13</td>
	         </tr>






				<tr>
					<th colspan='4' style="text-align:right;">
					<a href="javascript:void(0)" title="上一页" style="vertical-align:bottom" onclick="jumppage('0');return false"><<</a>&nbsp;&nbsp;<a href="javascript:void(0)" onclick="jumppage('1');return false"><font style='text-decoration:none;color:red'>1</font></a>&nbsp;&nbsp;<a href="javascript:void(0)" onclick="jumppage('2');return false">2</a>&nbsp;&nbsp;<a href="javascript:void(0)" title="下一页" style="vertical-align:bottom"  onclick="jumppage('2');return false">>></a>&nbsp;&nbsp;<input type="hidden" id="pageNo" name="pageNo" value='1' /><input type="hidden" value='2' id="pagescount"/><input type="hidden" id="pageSize" name="pageSize"  value='5' /><input type="hidden" id="clear" name="clear" />
				</th>
				</tr>

		</tbody>
	</table>
   </form>
</body>
</html>
'''

enterprise_html_beijing_gdxq = '''





<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet" />
	<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script><!-- 1.9版本jQuery js   -->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/pubInfo.js"></script><!-- 北京首页pubInfo.js js   -->
</head>

<body>
<div id="header"  style="height:119px;"><img src="/country_credit/bj/images/header_bj.jpg" width="990"/></div>
<br/>
	<div id="details" class="clear">
	<h2  style="background-color:#ce010c ;color:white;"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h2><!-- 注册号： -->
	<form action="gjjbj/gjjQueryCreditAction!touzirenInfo.dhtml" method="post"  name="iframeFrame" id="iframeFrame">
	<input type="hidden" id="pageNos" name="pageNos" value="1" />
	<input type="hidden" id="inv" name="chr_id" value="82062B55DBFD4C9B9921EEA44483EE25"/>
	   <div id="sifapanding" >
	<br>
	<table  cellpadding="0" cellspacing="0" class="detailsList">
		<tr><th colspan="9" style="text-align:center;">股东及出资信息 </th></tr>
        <tr width="95%">
		  <th width="10%" style="text-align:center;" rowspan="2">股东</th>
          <th width="13%" style="text-align:center;" rowspan="2">认缴额（万元）</th>
          <th width="13%" style="text-align:center;" rowspan="2">实缴额（万元）</th>
		  <th width="32%" style="text-align:center;" colspan="3">认缴明细</th>
          <th width="32%" style="text-align:center;" colspan="3">实缴明细</th>
        </tr>
         <tr width="95%">
		  <th width="10%" style="text-align:center;">认缴出资方式</th>
          <th width="10%" style="text-align:center;">认缴出资额（万元）</th>
          <th width="12%" style="text-align:center;">认缴出资日期</th>
		  <th width="10%" style="text-align:center;">实缴出资方式</th>
          <th width="10%" style="text-align:center;">实缴出资额（万元）</th>
		  <th width="12%" style="text-align:center;">实缴出资日期</th>
        </tr>

         	<tr>
			  <td style="text-align:left;"  >北京民营科技实业家协会</td>
	          <td style="text-align:right;" >50</td>
	          <td style="text-align:right;">50</td>
			  <td style="text-align:left;"></td>
	          <td style="text-align:right;">50</td>
	          <td style="text-align:center;"></td>
	          <td style="text-align:left;"></td>
	          <td style="text-align:right;">50</td>
			  <td style="text-align:center;"></td>
	        </tr>



			<tr><th colspan='9' style='text-align:right;'></th></tr>


	</table>
	</form></div>
<div id="footer"><img src="/country_credit/bj/images/footer_beijing1.jpg" width="990"/></div>
</body>
</html>'''

enterprise_html_jiangxi_fzjg = '''







<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>全国企业信用信息公示系统</title>
<link rel="stylesheet" type="text/css"
	href="http://gsxt.jxaic.gov.cn:80/ECPS//include/css/public3.css" />
<script type="text/javascript" src="/ECPS/include/js/jquery-1.9.0.min.js"></script>
<script type="text/javascript">
$(function(){
		var h = $("#main").height();
		if(!window.parent.document.getElementById('detailsCon4')){
			if(h < 780){
				h = 780;
			}
		}else{
			if(h < 970){
				h = 970;
			}
		}
		$("#detailsCon1",window.parent.document).css("height",h+50);
		$("#gsgsIframe",window.parent.document).css("height",h+20);
})
</script>
</head>

<body>
<div id="main">

	<br>
	<table style="width:100%; id=" t30" cellpadding="0" cellspacing="0"
		class="detailsList">
		<tr width="939px">
			<th colspan="6" style="text-align:center;">
				主要人员信息
			</th>
		</tr>
		<th style="width:10%;text-align:center">序号</th>
		<th style="width:20%;text-align:center">姓名</th>
		<th style="width:20%;text-align:center">职务</th>
		<th style="width:10%;text-align:center">序号</th>
		<th style="width:20%;text-align:center">姓名</th>
		<th style="width:20%;text-align:center">职务</th>
		</tr>



				<tr>
					<td style="text-align:center;">1</td>
					<td>曾敏</td>
					<td>监事</td>
					<td style="text-align:center;">2</td>
					<td>苏友明</td>
					<td>执行董事兼总经理</td>
				</tr>





	</table>
	<br>

	<table id="t31" cellpadding="0" cellspacing="0" class="detailsList">
		<tr width="939px">
			<th colspan="4" style="text-align:center;">分支机构信息</th>
		</tr>
		<tr>
			<th style="text-align:center;width:10%;">序号</th>
			<th style="text-align:center;width:25%">注册号/统一社会信用代码</th>
			<th style="text-align:center;width:25%">名称</th>
			<th style="text-align:center;width:20%">登记机关</th>
		</tr>

	</table>
	<br>

	<table id="t32" cellpadding="0" cellspacing="0" class="detailsList">
		<tr width="939px">
			<th colspan="4" style="text-align:center;">清算信息</th>
		</tr>
		<tr>
			<th style="width:20%">清算负责人</th>
			<td style="width:80%">

			</td>
		</tr>
		<tr>
			<th style="width:20%">清算组成员</th>
			<td style="width:80%">

			</td>
		</tr>

	</table>

</div>
</body>
</html>'''

enterprise_html_guangdong_gdxq = '''

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>企业信用信息公示系统</title>
    <link href="http://gsxt.gdgs.gov.cn/aiccips//css/public3.css" type="text/css" rel="stylesheet"/>
    <link rel="stylesheet" type="text/css" href="http://gsxt.gdgs.gov.cn/aiccips/css/style.css"/>
</head>

<body>
<form id="topForm" action="" method="post">
<input type="hidden" id="aiccipsUrl" value="http://gsxt.gdgs.gov.cn/aiccips/">
<input type="hidden" id="entNo" name="entNo" value="ad14832b-012b-1000-e000-07730a0c0115">
<input type="hidden" id="entType" name="entType" value="">
<input type="hidden" id="regOrg" name="regOrg" value="441900">
</form>
<div style="display: none;">
<script type="text/javascript" src="http://gsxt.gdgs.gov.cn/aiccips/js/cnzz.js"></script>
</div>
<div id="header" style="background-image: url('http://gsxt.gdgs.gov.cn/aiccips//images/header_02_gd.png');width:990px;height:125px;">
        <div class="top-a">
            <a href="http://gsxt.saic.gov.cn/">全国首页</a>
            <a href="#" onclick="window.open('http://gsxt.gdgs.gov.cn/aiccips/')">地方局首页</a>
        </div>
</div>
<div id="details" class="clear" style="height: 600px;text-align: left;">
<div style="text-align: left;height: 35px">
    <h2>东莞市中兆房地产开发有限公司&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;注册号：441900000911323</h2>
</div>  <br>
    <div id="jibenxinxi">
        <br>
        <table cellpadding="0" cellspacing="0" class="detailsList">
            <tr>
                <th colspan="8" style="text-align:center;">股东及出资信息</th>
            </tr>
            <tr width="95%">
                <th width="20%" style="text-align:center;">股东</th>
                <th width="10%" style="text-align:center;">股东类型</th>
                <th width="10%" style="text-align:center;">认缴出资额</th>
                <th width="10%" style="text-align:center;">出资方式</th>
                <th width="15%" style="text-align:center;">认缴出资日期</th>
                <th width="10%" style="text-align:center;">实缴出资额</th>
                <th width="10%" style="text-align:center;">出资方式</th>
                <th width="15%" style="text-align:center;">实缴出资时间</th>
            </tr>
            <tr>
                <td width="20%" style="text-align:center;">东莞市邦联实业投资有限公司</td>
                <td width="10%" style="text-align:center;">企业法人</td>
                <td width="10%" style="text-align:center;">100万人民币元</td>
                <td width="10%" style="text-align:center;">货币出资</td>
                <td width="15%" style="text-align:center;"></td>
                <td width="10%" style="text-align:center;">100万人民币元</td>
                <td width="10%" style="text-align:center;">货币出资</td>
                <td width="15%" style="text-align:center;">2010年10月11日</td>
            </tr>
        </table>
        <br/>
    </div>
</div>
<div style="width:990px;height:55px;text-align:center;margin:0 auto; padding-top:20px;font-size:14px;text-align:center; color:#fff;">
    <div class="banqun">
            版权所有：广东省工商行政管理局&nbsp;&nbsp;
        <a href="http://gsxt.gdgs.gov.cn:81/aiceps/portal/consult.html" target="_blank"  style="color: red;"><u>全省工商业务咨询电话</u>&nbsp;</a>
        <br> 地址：广州市天河区体育西路57号&nbsp;&nbsp;邮政编码：510620 &nbsp;&nbsp; 建议使用IE8及以上版本浏览器

    </div>
</div></body>
</html>
'''

enterprise_html_jiangxi_gdxx = '''







<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>全国企业信用信息公示系统</title>
	<link rel="stylesheet" type="text/css" href="http://gsxt.jxaic.gov.cn:80/ECPS//include/css/public3.css" />
	<link rel="stylesheet" type="text/css" href="http://gsxt.jxaic.gov.cn:80/ECPS//include/css/style.css"/>
	<link rel="stylesheet" type="text/css" href="http://gsxt.jxaic.gov.cn:80/ECPS//include/js/page/pageGroup.css"/>
	<script type="text/javascript" src="/ECPS/include/js/jquery-1.9.0.min.js"></script>
	<script type="text/javascript" src="http://gsxt.jxaic.gov.cn:80/ECPS//include/js/page/jquery-1.8.3.min.js"></script>
	<script type="text/javascript" src="http://gsxt.jxaic.gov.cn:80/ECPS//include/js/page/pageGroup.js"></script>
	<script type="text/javascript" src="/ECPS/include/js/pager.js"></script>
<script type="text/javascript">
$(function(){
		var h = $("#main").height();
		$("#gdxxf",window.parent.document).css("height",h);
		$("#gdxxIframe",window.parent.document).css("height",h);
})
</script>
</head>
<body>
<div id="main">
	<br/>
	<form action="/ECPS/ccjcgs/gsgs_viewDjxxGdxx.pt?qyid=3606002012081600243944" method="post">
	<table id="table3" cellspacing="0" cellpadding="0" class="detailsList" >
		<tr>
			<th colspan="5" style="text-align:center;">

					发起人信息

				<br>
				<h1 style="text-align:center;">股东的出资信息截止2014年2月28日。2014年2月28日之后工商只公示股东姓名，其他出资信息由企业自行公示。</h1>
			</th>
		</tr>
		<tbody id="table3">
			<tr width="95%">
				<th width="20%" style="text-align:center;">

					发起人类型



				</th>
				<th width="20%" style="text-align:center;">

					发起人


				</th>
				<th width="20%" style="text-align:center;">证照/证件类型</th>
				<th width="20%" style="text-align:center;">证照/证件号码</th>

					发起人


				</th>

			</tr>


				<tr>
					<td>自然人股东</td>
					<td>吴茂盛</td>
					<td>
					中华人民共和国居民身份证
					</td>
					<td>

						***
					</td>

				</tr>

				<tr>
					<td>法人股东</td>
					<td>鹰潭市金海贸易有限公司</td>
					<td>企业法人营业执照(公司)

					</td>
					<td>
						360600210014860

					</td>

				</tr>

				<tr>
					<td>法人股东</td>
					<td>鹰潭市月湖区新鑫工贸有限公司</td>
					<td>

					</td>
					<td>
						360602210008871

					</td>

				</tr>

				<tr>
					<td>自然人股东</td>
					<td>邓华成</td>
					<td>
					中华人民共和国居民身份证
					</td>
					<td>

						***
					</td>

				</tr>

				<tr>
					<td>自然人股东</td>
					<td>许友全</td>
					<td>
					中华人民共和国居民身份证
					</td>
					<td>

						***
					</td>

				</tr>



			<tr>
				<th colspan="5">
					<script type="text/javascript">
						getPager2('9','2','1','5');
				  	</script>
				  	<input type="hidden" id="totalPage" value="2" />
				  	<input type="hidden" id="pageNum" value="1" />
				  	<input type="hidden" id="mark" name="mark" value="" />
				</th>
			</tr>

		</tbody>
	</table>

</form>
</div>
</body>
</html>
'''

enterprise_html_jiangxi_zyry = '''







<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>全国企业信用信息公示系统</title>
<link rel="stylesheet" type="text/css"
	href="http://gsxt.jxaic.gov.cn:80/ECPS//include/css/public3.css" />
<script type="text/javascript" src="/ECPS/include/js/jquery-1.9.0.min.js"></script>
<script type="text/javascript">
$(function(){
		var h = $("#main").height();
		if(!window.parent.document.getElementById('detailsCon4')){
			if(h < 780){
				h = 780;
			}
		}else{
			if(h < 970){
				h = 970;
			}
		}
		$("#detailsCon1",window.parent.document).css("height",h+50);
		$("#gsgsIframe",window.parent.document).css("height",h+20);
})
</script>
</head>

<body>
<div id="main">

	<br>
	<table style="width:100%; id=" t30" cellpadding="0" cellspacing="0"
		class="detailsList">
		<tr width="939px">
			<th colspan="6" style="text-align:center;">
				主要人员信息
			</th>
		</tr>
		<th style="width:10%;text-align:center">序号</th>
		<th style="width:20%;text-align:center">姓名</th>
		<th style="width:20%;text-align:center">职务</th>
		<th style="width:10%;text-align:center">序号</th>
		<th style="width:20%;text-align:center">姓名</th>
		<th style="width:20%;text-align:center">职务</th>
		</tr>



				<tr>
					<td style="text-align:center;">1</td>
					<td>胡志军</td>
					<td>董事</td>
					<td style="text-align:center;">2</td>
					<td>许光锦</td>
					<td>董事</td>
				</tr>





				<tr>
					<td style="text-align:center;">3</td>
					<td>胡逢林</td>
					<td>董事</td>
					<td style="text-align:center;">4</td>
					<td>苏坚毅</td>
					<td>董事</td>
				</tr>





				<tr>
					<td style="text-align:center;">5</td>
					<td>胡逢水</td>
					<td>董事长</td>
					<td style="text-align:center;">6</td>
					<td>李华</td>
					<td>董事</td>
				</tr>





				<tr>
					<td style="text-align:center;">7</td>
					<td>管荣荣</td>
					<td>监事</td>
					<td style="text-align:center;">8</td>
					<td>吴茂盛</td>
					<td>监事</td>
				</tr>





				<tr>
					<td style="text-align:center;">9</td>
					<td>刘江</td>
					<td>监事</td>
					<td style="text-align:center;">10</td>
					<td>陈洁</td>
					<td>总经理</td>
				</tr>





	</table>
	<br>

	<table id="t31" cellpadding="0" cellspacing="0" class="detailsList">
		<tr width="939px">
			<th colspan="4" style="text-align:center;">分支机构信息</th>
		</tr>
		<tr>
			<th style="text-align:center;width:10%;">序号</th>
			<th style="text-align:center;width:25%">注册号/统一社会信用代码</th>
			<th style="text-align:center;width:25%">名称</th>
			<th style="text-align:center;width:20%">登记机关</th>
		</tr>

	</table>
	<br>

	<table id="t32" cellpadding="0" cellspacing="0" class="detailsList">
		<tr width="939px">
			<th colspan="4" style="text-align:center;">清算信息</th>
		</tr>
		<tr>
			<th style="width:20%">清算负责人</th>
			<td style="width:80%">

			</td>
		</tr>
		<tr>
			<th style="width:20%">清算组成员</th>
			<td style="width:80%">

			</td>
		</tr>

	</table>

</div>
</body>
</html>
'''

en_beijing_qynb = '''



<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>全国企业信用信息公示系统</title>
<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet" />
<link href="/country_credit/bj/css/style.css" type="text/css" rel="stylesheet" />
<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script>
<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/pubInfo.js"></script>
<script >
$(function(){

    var zd = [];
    $(".color_zd").each(function(){
        zd.push($(this).attr('id'));
    });

    if(zd.length > 0){
	    	jQuery.ajax({
	            type: "post",
	             url: "/entPub/entPubAction!getZdbgIsExist.dhtml",
	            data: {'zd':zd.join(',')},
	            dataType: "json",
	            async:true,
	            success: function(data){
	                if(data && data.returnCode && data.list.length > 0){
		                 $.each(data.list,function(index,enty){
                             $("#"+enty.cid+'_'+enty.tb+'_'+enty.zd).css("color","red");
			             });
		            }
	            },
	            error: function(){
	            	alert("提示：服务异常，请重试！");
	            }
	        });
	}

});
</script>
</head>
<body>
<div id="header">
	<div class="top">
		<div class="top-a">
			<!-- <a href="#"  onclick="toCountryIndex();">全国首页</a>
			<a href="#" onclick="toIndex();">地方局首页</a> -->
		 </div>
	</div>
</div>
<div id="details" class="clear">
        <h2 id="gsh2">
         安邦保险集团股份有限公司 &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp; 注册号/统一社会信用代码：100000000040274&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
   </h2><br/>
<div id="sifapanding" >
<div id="sifapanding" >
	<!-- 企业基本信息      begin    -->
	<div id="qufenkuang" style ="border:solid 1px grey;">
	<table  cellpadding="0" cellspacing="0" class="detailsList">
		<tr><th colspan="4" style="text-align:center;color:#000">2013年度报告</th></tr>
		<tr><th colspan="4" style="text-align:center;color:#000">企业基本信息</th></tr>
        <tr>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_1_regno">注册号/统一社会信用代码</th><td width="30%">100000000040274</td>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_1_entname">企业名称</th><td width="30%">安邦保险集团股份有限公司</td>
        </tr>

        <!-- 1和6类型的展示页面    begin -->

		 <tr>
		 <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_1_tel">企业联系电话</th>
         <td width="30%">95569</td>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_1_postalcode">邮政编码</th>
         <td width="30%">100022</td>
        </tr>
	    <tr>
         <th width="20%"  class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_1_addr">企业通信地址</th>
         <td colspan="3">北京市朝阳区建国门外大街6号12层1202</td>
        </tr>
		<tr>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_1_email">电子邮箱</th>
         <td width="30%">Jt_office@ab-insurance.com</td>


	         <th width="20%"  class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_1_isownercha"></th>
	         <td width="30%"> </td>

        </tr>
		<tr>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_1_busstValue">企业经营状态</th>
         <td width="30%"> 开业</td>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_1_isweb">是否有网站或网店</th>
          <td width="30%">是</td>
        </tr>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_1_isinv">企业是否有投资信息或购买其他公司股权</th>
        <td width="30%">无</td>
		 <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_1_empnum">从业人数</th>
        <td width="30%">企业选择不公示</td>


		<!-- 2和7类型的展示页面    begin -->

      	<!-- 3和5类型的展示页面    begin   4是个体，单写的页面-->

	</table>
	<!-- 企业基本信息      end    -->

	<!-- 如果存在站和网店，就将网站和网店列出，否则，不列出   OK-->

      		<div style="float:left;width:100%;margin-top:20px;height:auto;">
				  <iframe id="wzFrame" src='/entPub/entPubAction!wz_bj.dhtml?clear=true&cid=72cc0c5319274ba8ac2a8ce3758d2eaa' scrolling="no"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
            </div>


        <!-- 类型是1 和6 的，将股东及出资信息列出  OK-->

		    <div style="float:left;width:100%;margin-top:20px;height:auto;">
				<iframe id="gdczFrame"  src='/entPub/entPubAction!gdcz_bj.dhtml?clear=true&cid=72cc0c5319274ba8ac2a8ce3758d2eaa&entnature=' scrolling="no"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
	      	</div>

        <!-- 类型为1 2 4 7 并且存在股东信息，将对外投资信息列出   OK-->




       <!-- 企业资产状况信息   类型1,2 ,6,7 -->

		<table  cellpadding="0" cellspacing="0" class="detailsList">
		<tr><th colspan="4" style="text-align:center;">企业资产状况信息</th></tr>

        <tr>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_2_assgro">资产总额</th>
         <td width="30%">


         			企业选择不公示

         </td>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_2_totequ">所有者权益合计</th>
         <td width="30%">


         			企业选择不公示

         </td>
        </tr>
        <tr>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_2_vendinc">销售总额</th>
		 <td width="30%">


         			企业选择不公示

		 </td>
		 <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_2_progro">利润总额</th>
		 <td width="30%">


         			企业选择不公示

		 </td>
        </tr>
	    <tr>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_2_maibusinc">营业总收入中主营业务收入</th>
		 <td width="30%">


         			企业选择不公示

		 </td>
		 <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_2_netinc">净利润</th>
		 <td width="30%">


         			企业选择不公示

		 </td>
        </tr>
	    <tr>
         <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_2_ratgro">纳税总额</th>
		 <td width="30%">


         			企业选择不公示

		 </td>
		 <th width="20%" class="color_zd" id="72cc0c5319274ba8ac2a8ce3758d2eaa_2_liagro">负债总额</th>
		 <td width="30%">


         			企业选择不公示

		 </td>
        </tr>

	</table><br/>


       <!-- 企业资产状况信息   类型3,5 -->

	<br>
	<!-- 企业对外担保信息 -->
	<div style="float:left;width:100%;margin-top:20px;height:auto;"><!-- entPub/entPubAction! -->
		<iframe  id="dwdbFrame"   src='/entPub/entPubAction!qydwdb_bj.dhtml?clear=true&cid=72cc0c5319274ba8ac2a8ce3758d2eaa' scrolling="no"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
	</div>

	 <!-- 股权变更信息  股权变更信息 -->



	</div>
	<br/>
	<!-- 修改记录 -->
	<div id="qufenkuang" style =" margin-top:20px;">
		<iframe  id="xgFrame"  src='/entPub/entPubAction!qybg_bj.dhtml?clear=true&cid=72cc0c5319274ba8ac2a8ce3758d2eaa&year=2013' scrolling="no"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
	</div>
	<br/>
	<br/>

<div class="banqun" style="padding-bottom:20px;margin-top:10px;">
              版权所有：北京市工商行政管理局&nbsp;&nbsp;&nbsp;&nbsp;地址：北京市海淀区苏州街36号&nbsp;&nbsp;&nbsp;&nbsp;邮政编码：100080<br />
              <!-- 业务咨询电话：010-82691213，010-82691523&nbsp;&nbsp;&nbsp;&nbsp;技术支持电话：010-82691768（公示），010-82691101（年报） -->
</div>
<div style="display:none;">
<script src="http://s4.cnzz.com/z_stat.php?id=1257386840&web_id=1257386840" language="JavaScript"></script>
</div>
 </div>
</body>
</html>
'''

en_guangdong_gz = '''

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>企业信用信息公示系统</title>
<link href="http://gsxt.gzaic.gov.cn/aiccips//css/public3.css" type="text/css" rel="stylesheet" />
    <link rel="stylesheet" type="text/css" href="http://gsxt.gzaic.gov.cn/aiccips/css/style.css"/>
    <link rel="stylesheet" type="text/css" href="http://gsxt.gzaic.gov.cn/aiccips/css/style.css"/>
    <script type="text/javascript">
        function init(){
            document.getElementById("left1").className="current";
            if(document.getElementById("left2"))document.getElementById("left2").className="";
//            document.getElementById("left3").className="";
            changeStyle('tabs','0');
        }
    </script>
</head>

<body onload="init()">
<form id="topForm" action="" method="post">
<input type="hidden" id="aiccipsUrl" value="http://gsxt.gzaic.gov.cn/aiccips/">
<input type="hidden" id="entNo" name="entNo" value="440111111022011042900502">
<input type="hidden" id="entType" name="entType" value="1130">
<input type="hidden" id="regOrg" name="regOrg" value="440126">
</form>
<div style="display: none;">
<script type="text/javascript" src="http://gsxt.gzaic.gov.cn/aiccips/js/cnzz.js"></script>
</div>
<div id="header" style="background-image: url('http://gsxt.gzaic.gov.cn/aiccips//images/header_02_gd.png');width:990px;height:125px;">
        <div class="top-a">
            <a href="http://gsxt.saic.gov.cn/">全国首页</a>
            <a href="#" onclick="window.open('http://gsxt.gzaic.gov.cn/aiccips/')">地方局首页</a>
        </div>
</div>
<div id="details" class="clear" >
<script type="text/javascript" src="http://gsxt.gzaic.gov.cn/aiccips/easyui/jquery-1.7.2.min.js"></script>
<script type="text/javascript" src="http://gsxt.gzaic.gov.cn/aiccips/js/loading/loading.s.js"></script>
<script type="text/javascript">
    function goIndex() {
        var entName =  encodeURI("广州骏速新能源科技有限公司");
        var entNo = encodeURI("440111111022011042900502");
        var regOrg = encodeURI("440126");
        open("http://gsxt.gzaic.gov.cn/aiccips/Inform/InformLogin.html?regNo=440111000275031&entName="+entName+"&entNo="+entNo+"&regOrg="+regOrg);
    }
</script>
<div style="text-align: left;height: 45px">
            <h2 style="height: 25px">
            广州骏速新能源科技有限公司&nbsp;&nbsp;&nbsp;&nbsp;注册号/统一社会信用代码：9144011357402815XW
            </h2>

</div>  <br>
  <div id="leftTabs">
      <input type="hidden" style="width:99%;background-color:#efefef;"  id="entNo"   name="entNo" value="440111111022011042900502"/>
      <ul>
                  <li id="left1" class="current" onclick="togo('1')" style="margin-bottom:2px;"><p class="font15">工<br />商<br />公<br />示<br />信<br />息</p></li>
                            <li id="left2" class="" onclick="togo('2')"><p class="font15">企<br />业<br />公<br />示<br />信<br />息</p></li>
                  <li  style="height:300px" id="left3" class="" onclick="togo('3')"><p class="font15">其<br />他<br />部<br />门<br />公<br />示<br />信<br />息</p></li>
                          <li  id="left4" class="" onclick="togo('4')" ><p class="font15"  style="margin-top: -50px">司<br />法<br />协<br />助<br />公<br />示<br />信<br />息</p></li>
    </ul>
  </div>
  <script type="text/javascript">
      function togo(str){
          showLoading();
          var url = "";
          if(str=='1'){
              url='http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entInfo';
          }else if(str=='2'){
              url='http://gsxt.gzaic.gov.cn/aiccips/BusinessAnnals/BusinessAnnalsList.html';
          }else if(str=='3'){
              //url='http://gsxt.gzaic.gov.cn/aiccips/OtherPublicity/environmentalProtection.html';
                  url='http://gsxt.gzaic.gov.cn/aiccips/OtherPublicity/environmentalProtection.html';
          }else if(str=='4'){
              //url='http://gsxt.gzaic.gov.cn/aiccips/judiciaryAssist/judiciaryAssistInit.html';
                  url='http://gsxt.gzaic.gov.cn/aiccips/judiciaryAssist/judiciaryAssistInit.html';
          }
          if(url!=""){
              $("#topForm").serialize();
              $('#topForm').attr('action', url);
              $("#topForm").submit();
          }else{
              hidenLoading();
          }
      }
  </script>    <div id="detailsCon">
        <div class="dConBox">


      <div class="tabs" id="tabs">

             <li id="0" class="current" onclick="r0('0')">登记信息</li>
             <li id="2" class="" onclick="r0('2')">备案信息</li>

          <li id="4" onclick="r0('4')">动产抵押登记信息</li>
              <li id="3" onclick="r0('3')">股权出质登记信息</li>
            <li id="7" onclick="r0('7')">行政处罚信息</li>
            <li id="5" onclick="r0('5')">经营异常信息</li>
                <li id="6" onclick="r0('6')"> 严重违法失信信息</li>

            <li id="8" onclick="r0('8')">抽查检查信息</li>
      </div>

      <script type="text/javascript">
          function r0(id){
              showLoading();
              var url = "";
              if(id=='0'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entInfo";
              }else if(id=='1'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entChaInfo";
              }else if(id=='2'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entCheckInfo";
              }else if(id=='3'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=curStoPleInfo";
              }else if(id=='4'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=pleInfo";
              }else if(id=='5'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=cipUnuDirInfo";
              }else if(id=='6'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=cipBlackInfo";
              }else if(id=='7'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=cipPenaltyInfo";
              }else if(id=='8'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=cipSpotCheInfo";
              }else if(id=='10'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=twadm";
              }else if(id=='11'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=twcredit";
              }

              if(url!=""){
                  $("#topForm").serialize();
                  $('#topForm').attr('action', url);
                  $("#topForm").submit();
              }else{
                  hidenLoading();
              }
          }
          function toPages(pageNo,baseHref,url){
              var aiccipsUrl = "&aiccipsUrl="+$("#aiccipsUrl").val();
              var entNo = "&entNo="+$("#entNo").val();
              var entType = "&entType="+$("#entType").val();
              var regOrg = "&regOrg="+$("#regOrg").val();
              window.location.href = baseHref+url+"&pageNo="+pageNo+entNo+aiccipsUrl+entType+regOrg;
          }
          function t0(){
              document.getElementById('baseinfo').style.display='block';
              document.getElementById('touziren').style.display='none';
          }

          function t1(){
              document.getElementById('baseinfo').style.display='none';
              document.getElementById('touziren').style.display='block';
          }

          function t30(){
              document.getElementById('t30').style.display='block';
              document.getElementById('t31').style.display='none';
              document.getElementById('t32').style.display='none';
          }

          function t31(){
              document.getElementById('t30').style.display='none';
              document.getElementById('t31').style.display='block';
              document.getElementById('t32').style.display='none';

          }

          function t32(){
              document.getElementById('t30').style.display='none';
              document.getElementById('t31').style.display='none';
              document.getElementById('t32').style.display='block';
              changeStyle('beian','32');
          }

          function changeStyle(divId,ele){
              var liAry=document.getElementById(divId).getElementsByTagName("li");
              var liLen=liAry.length;
              var liID=ele;
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
      </script>





      <div id="jibenxinxi"  style="height:980px;overflow:auto;">

           <table cellspacing="0" cellpadding="0" class="detailsList" id="baseinfo">
      	<tr><th colspan="4" style="text-align:center;">基本信息 </th></tr>
        <tr>
            <th width="20%">统一社会信用代码</th>
            <td colspan="3">9144011357402815XW</td>
        </tr>
        <tr>
            <th width="20%">注册号</th>
            <td width="30%">440111000275031</td>
          <th>名称</th>
          <td width="30%">广州骏速新能源科技有限公司</td>
        </tr>
        <tr>
          <th>类型</th>
          <td>有限责任公司(自然人投资或控股)</td>
          <th width="20%">法定代表人</th>
          <td>林忠明</td>
        </tr>
        <tr>
          <th width="20%">注册资本</th>
          <td>100万</td>
          <th>成立日期</th>
          <td>2011年05月09日</td>
        </tr>
        <tr>
          <th>经营场所</th>
          <td colspan="3">广州市番禺区东环街龙美村巷尾ABC厂房号A2之一</td>
        </tr>
          <tr>
              <th>营业期限自</th>
              <td>2011年05月09日</td>
              <th>营业期限至</th>
              <td>
                            长期
              </td>
          </tr>
        <tr>
          <th>经营范围</th>
          <td colspan="3">能源技术研究、技术开发服务;环保技术推广服务;环保技术开发服务;环保技术咨询、交流服务;环保技术转让服务;能源技术咨询服务;润滑油批发;润滑油零售;沥青及其制品销售;商品批发贸易（许可审批类商品除外）;商品零售贸易（许可审批类商品除外）;货物进出口（专营专控商品除外）;技术进出口;<br><br>(依法须经批准的项目，经相关部门批准后方可开展经营活动)〓
          </td>
        </tr>
          <tr>
              <th>登记机关</th>
              <td>广州市工商行政管理局番禺分局</td>
              <th>核准日期</th>
              <td>2016年02月23日</td>
          </tr>

         <tr>
        	<th>登记状态</th>
          <td>存续</td>
          <th></th>
          <td></td>
        </tr>
      </table>
        </br>
<table  cellpadding="0" cellspacing="0" class="detailsList" id="touzirentop" style="" >
    <tr>
        <th colspan="6" style="text-align:center;">股东信息<br/><span>股东的出资信息截止2014年2月28日。2014年2月28日之后工商只公示股东姓名，其他出资信息由企业自行公示。</span></th>
    </tr>
    <tr width="95%">

               <th width="20%" style="text-align:center;">股东类型</th>
        <th width="20%" style="text-align:center;">股东</th>
        <th width="25%" style="text-align:center;">证照/证件类型</th>
        <th width="25%" style="text-align:center;">证照/证件号码</th>
        <th width="10%" style="text-align:center;">详情</th>

</tr>
</table>
<div style="border:1px solid #ccc;" id="invInfo">
<table  cellpadding="0" cellspacing="0" class="detailsList" id="touziren" style="" >
           <tr>
               <td width="20%" style="text-align:center;">自然人股东</td>
               <td width="20%" style="text-align:center;">房静</td>
               <td width="25%" style="text-align:center;"></td>
               <td width="25%" style="text-align:center;">不公示</td>
               <td width="10%" style="text-align:center;">
                        <a href="#" onclick="window.open('http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/invInfoDetails.html?invNo=6622555C-CFA5-3E0A-29DD-13BD493D196B&entNo=440111111022011042900502&regOrg=440126')">详情</a>
                </td>
            </tr>
           <tr>
               <td width="20%" style="text-align:center;">企业法人</td>
               <td width="20%" style="text-align:center;">广东精钢盾环保能源科技有限公司</td>
               <td width="25%" style="text-align:center;"></td>
               <td width="25%" style="text-align:center;"></td>
               <td width="10%" style="text-align:center;">
                        <a href="#" onclick="window.open('http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/invInfoDetails.html?invNo=9215CD86-B36C-6F56-D685-CB96248111D5&entNo=440111111022011042900502&regOrg=440126')">详情</a>
                </td>
            </tr>
           <tr>
               <td width="20%" style="text-align:center;">自然人股东</td>
               <td width="20%" style="text-align:center;">王奔</td>
               <td width="25%" style="text-align:center;"></td>
               <td width="25%" style="text-align:center;">不公示</td>
               <td width="10%" style="text-align:center;">
                        <a href="#" onclick="window.open('http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/invInfoDetails.html?invNo=BABFD5FB-823A-B21E-AE56-E272309788F2&entNo=440111111022011042900502&regOrg=440126')">详情</a>
                </td>
            </tr>
    </table>
        <table  cellpadding="0" cellspacing="0" class="detailsList">
            <tr><th colspan="6" style="text-align:right;">
                    <<&nbsp; &nbsp;
                1/1&nbsp;&nbsp;
                    >>
            </th></tr>
        </table>
</div>




          </br>
<table  cellpadding="0" cellspacing="0" class="detailsList">
    <tr width="95%"><th colspan="4" style="text-align:center;">变更信息</th></tr>
    <tr width="95%">
        <th width="15%" style="text-align:center;"> 变更事项</th>
        <th width="35%" style="text-align:center;"> 变更前内容</th>
        <th width="35%" style="text-align:center;"> 变更后内容</th>
        <th width="15%" style="text-align:center;"> 变更日期</th>
    </tr>
</table>
<div id="biangeng" style="border:1px solid #ccc;">
        <table  cellpadding="0" cellspacing="0" class="detailsList">
                        <tr width="95%">
                <td width="15%" style="text-align:center;">执照副本变更</td>
                <td width="35%" style="text-align:center;">1</td>
                <td width="35%" style="text-align:center;">2</td>
                <td width="15%" style="text-align:center;">2016年02月23日</td>
            </tr>
            <tr width="95%">
                <td width="15%" style="text-align:center;">章程备案</td>
                <td width="35%" style="text-align:center;">章程备案(变更前)</td>
                <td width="35%" style="text-align:center;">准予章程备案</td>
                <td width="15%" style="text-align:center;">2016年02月23日</td>
            </tr>
            <tr width="95%">
                <td width="15%" style="text-align:center;">营业期限变更</td>
                <td width="35%" style="text-align:center;">2011-05-09 至 2016-02-03</td>
                <td width="35%" style="text-align:center;">2011-05-09 至</td>
                <td width="15%" style="text-align:center;">2016年02月23日</td>
            </tr>
    <tr width="95%">
            <table  cellpadding="0" cellspacing="0" class="detailsList">
                <tr><th colspan="6" style="text-align:right;">
                        <<&nbsp;&nbsp;
                1/1&nbsp;&nbsp;
                        >>
                </th></tr>
            </table>
    </tr>
    </table>

</div>
           </br>
            </div>
		</div>
    </div>
    <br><br>
  </div>
﻿<div style="width:990px;height:55px;text-align:center;margin:0 auto; padding-top:20px;font-size:14px;text-align:center; color:#fff;">
    <div class="banqun">
            版权所有：广东省工商行政管理局&nbsp;&nbsp;
        <a href="http://gsxt.gdgs.gov.cn:81/aiceps/portal/consult.html" target="_blank"  style="color: red;"><u>全省工商业务咨询电话</u>&nbsp;</a>
        <br> 地址：广州市天河区体育西路57号&nbsp;&nbsp;邮政编码：510620 &nbsp;&nbsp; 建议使用IE8及以上版本浏览器
<script src="http://s4.cnzz.com/z_stat.php?id=1258472182&web_id=1258472182" language="JavaScript"></script>
    </div>

</div></body>
</html>
'''

en_guangdong_gz2 = '''

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>企业信用信息公示系统</title>
<link href="http://gsxt.gzaic.gov.cn/aiccips//css/public3.css" type="text/css" rel="stylesheet" />
    <link rel="stylesheet" type="text/css" href="http://gsxt.gzaic.gov.cn/aiccips/css/style.css"/>
    <link rel="stylesheet" type="text/css" href="http://gsxt.gzaic.gov.cn/aiccips/css/style.css"/>
    <script type="text/javascript">
        function init(){
            document.getElementById("left1").className="current";
            if(document.getElementById("left2"))document.getElementById("left2").className="";
//            document.getElementById("left3").className="";
            changeStyle('tabs','0');
        }
    </script>
</head>

<body onload="init()">
<form id="topForm" action="" method="post">
<input type="hidden" id="aiccipsUrl" value="http://gsxt.gzaic.gov.cn/aiccips/">
<input type="hidden" id="entNo" name="entNo" value="440100100042003093000735">
<input type="hidden" id="entType" name="entType" value="1152">
<input type="hidden" id="regOrg" name="regOrg" value="440100">
</form>
<div style="display: none;">
<script type="text/javascript" src="http://gsxt.gzaic.gov.cn/aiccips/js/cnzz.js"></script>
</div>
<div id="header" style="background-image: url('http://gsxt.gzaic.gov.cn/aiccips//images/header_02_gd.png');width:990px;height:125px;">
        <div class="top-a">
            <a href="http://gsxt.saic.gov.cn/">全国首页</a>
            <a href="#" onclick="window.open('http://gsxt.gzaic.gov.cn/aiccips/')">地方局首页</a>
        </div>
</div>
<div id="details" class="clear" >
<script type="text/javascript" src="http://gsxt.gzaic.gov.cn/aiccips/easyui/jquery-1.7.2.min.js"></script>
<script type="text/javascript" src="http://gsxt.gzaic.gov.cn/aiccips/js/loading/loading.s.js"></script>
<script type="text/javascript">
    function goIndex() {
        var entName =  encodeURI("广州顺丰速运有限公司");
        var entNo = encodeURI("440100100042003093000735");
        var regOrg = encodeURI("440100");
        open("http://gsxt.gzaic.gov.cn/aiccips/Inform/InformLogin.html?regNo=440101400011332&entName="+entName+"&entNo="+entNo+"&regOrg="+regOrg);
    }
</script>
<div style="text-align: left;height: 45px">
            <h2 style="height: 25px">
            广州顺丰速运有限公司&nbsp;&nbsp;&nbsp;&nbsp;注册号/统一社会信用代码：914401017248329968
            </h2>

</div>  <br>
  <div id="leftTabs">
      <input type="hidden" style="width:99%;background-color:#efefef;"  id="entNo"   name="entNo" value="440100100042003093000735"/>
      <ul>
                  <li id="left1" class="current" onclick="togo('1')" style="margin-bottom:2px;"><p class="font15">工<br />商<br />公<br />示<br />信<br />息</p></li>
                            <li id="left2" class="" onclick="togo('2')"><p class="font15">企<br />业<br />公<br />示<br />信<br />息</p></li>
                  <li  style="height:300px" id="left3" class="" onclick="togo('3')"><p class="font15">其<br />他<br />部<br />门<br />公<br />示<br />信<br />息</p></li>
                          <li  id="left4" class="" onclick="togo('4')" ><p class="font15"  style="margin-top: -50px">司<br />法<br />协<br />助<br />公<br />示<br />信<br />息</p></li>
    </ul>
  </div>
  <script type="text/javascript">
      function togo(str){
          showLoading();
          var url = "";
          if(str=='1'){
              url='http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entInfo';
          }else if(str=='2'){
              url='http://gsxt.gzaic.gov.cn/aiccips/BusinessAnnals/BusinessAnnalsList.html';
          }else if(str=='3'){
              //url='http://gsxt.gzaic.gov.cn/aiccips/OtherPublicity/environmentalProtection.html';
                  url='http://gsxt.gzaic.gov.cn/aiccips/OtherPublicity/environmentalProtection.html';
          }else if(str=='4'){
              //url='http://gsxt.gzaic.gov.cn/aiccips/judiciaryAssist/judiciaryAssistInit.html';
                  url='http://gsxt.gzaic.gov.cn/aiccips/judiciaryAssist/judiciaryAssistInit.html';
          }
          if(url!=""){
              $("#topForm").serialize();
              $('#topForm').attr('action', url);
              $("#topForm").submit();
          }else{
              hidenLoading();
          }
      }
  </script>    <div id="detailsCon">
        <div class="dConBox">


      <div class="tabs" id="tabs">

             <li id="0" class="current" onclick="r0('0')">登记信息</li>
             <li id="2" class="" onclick="r0('2')">备案信息</li>

          <li id="4" onclick="r0('4')">动产抵押登记信息</li>
              <li id="3" onclick="r0('3')">股权出质登记信息</li>
            <li id="7" onclick="r0('7')">行政处罚信息</li>
            <li id="5" onclick="r0('5')">经营异常信息</li>
                <li id="6" onclick="r0('6')"> 严重违法失信信息</li>

            <li id="8" onclick="r0('8')">抽查检查信息</li>
      </div>

      <script type="text/javascript">
          function r0(id){
              showLoading();
              var url = "";
              if(id=='0'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entInfo";
              }else if(id=='1'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entChaInfo";
              }else if(id=='2'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entCheckInfo";
              }else if(id=='3'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=curStoPleInfo";
              }else if(id=='4'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=pleInfo";
              }else if(id=='5'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=cipUnuDirInfo";
              }else if(id=='6'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=cipBlackInfo";
              }else if(id=='7'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=cipPenaltyInfo";
              }else if(id=='8'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=cipSpotCheInfo";
              }else if(id=='10'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=twadm";
              }else if(id=='11'){
                  url = "http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=twcredit";
              }

              if(url!=""){
                  $("#topForm").serialize();
                  $('#topForm').attr('action', url);
                  $("#topForm").submit();
              }else{
                  hidenLoading();
              }
          }
          function toPages(pageNo,baseHref,url){
              var aiccipsUrl = "&aiccipsUrl="+$("#aiccipsUrl").val();
              var entNo = "&entNo="+$("#entNo").val();
              var entType = "&entType="+$("#entType").val();
              var regOrg = "&regOrg="+$("#regOrg").val();
              window.location.href = baseHref+url+"&pageNo="+pageNo+entNo+aiccipsUrl+entType+regOrg;
          }
          function t0(){
              document.getElementById('baseinfo').style.display='block';
              document.getElementById('touziren').style.display='none';
          }

          function t1(){
              document.getElementById('baseinfo').style.display='none';
              document.getElementById('touziren').style.display='block';
          }

          function t30(){
              document.getElementById('t30').style.display='block';
              document.getElementById('t31').style.display='none';
              document.getElementById('t32').style.display='none';
          }

          function t31(){
              document.getElementById('t30').style.display='none';
              document.getElementById('t31').style.display='block';
              document.getElementById('t32').style.display='none';

          }

          function t32(){
              document.getElementById('t30').style.display='none';
              document.getElementById('t31').style.display='none';
              document.getElementById('t32').style.display='block';
              changeStyle('beian','32');
          }

          function changeStyle(divId,ele){
              var liAry=document.getElementById(divId).getElementsByTagName("li");
              var liLen=liAry.length;
              var liID=ele;
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
      </script>





      <div id="jibenxinxi"  style="height:980px;overflow:auto;">

           <table cellspacing="0" cellpadding="0" class="detailsList" id="baseinfo">
      	<tr><th colspan="4" style="text-align:center;">基本信息 </th></tr>
        <tr>
            <th width="20%">统一社会信用代码</th>
            <td colspan="3">914401017248329968</td>
        </tr>
        <tr>
            <th width="20%">注册号</th>
            <td width="30%">440101400011332</td>
          <th>名称</th>
          <td width="30%">广州顺丰速运有限公司</td>
        </tr>
        <tr>
          <th>类型</th>
          <td>有限责任公司(法人独资)</td>
          <th width="20%">法定代表人</th>
          <td>陶志刚</td>
        </tr>
        <tr>
          <th width="20%">注册资本</th>
          <td>9484.3682万</td>
          <th>成立日期</th>
          <td>2000年11月07日</td>
        </tr>
        <tr>
          <th>经营场所</th>
          <td colspan="3">广州市越秀区东风东路776号3-4楼全层</td>
        </tr>
          <tr>
              <th>营业期限自</th>
              <td>2000年11月07日</td>
              <th>营业期限至</th>
              <td>
                            2020年11月07日
              </td>
          </tr>
        <tr>
          <th>经营范围</th>
          <td colspan="3">国际快递业务;跨省快递业务;省内快递业务;道路货物运输;国际货运代理;货物进出口（专营专控商品除外）;技术进出口;广告业;其他仓储业（不含原油、成品油仓储、燃气仓储、危险品仓储）;<br><br>(依法须经批准的项目，经相关部门批准后方可开展经营活动)〓
          </td>
        </tr>
          <tr>
              <th>登记机关</th>
              <td>广州市工商行政管理局</td>
              <th>核准日期</th>
              <td>2016年05月10日</td>
          </tr>

         <tr>
        	<th>登记状态</th>
          <td>存续</td>
          <th></th>
          <td></td>
        </tr>
      </table>
        </br>
<table  cellpadding="0" cellspacing="0" class="detailsList" id="touzirentop" style="" >
    <tr>
        <th colspan="6" style="text-align:center;">股东信息<br/><span>股东的出资信息截止2014年2月28日。2014年2月28日之后工商只公示股东姓名，其他出资信息由企业自行公示。</span></th>
    </tr>
    <tr width="95%">

               <th width="20%" style="text-align:center;">股东类型</th>
        <th width="20%" style="text-align:center;">股东</th>
        <th width="25%" style="text-align:center;">证照/证件类型</th>
        <th width="25%" style="text-align:center;">证照/证件号码</th>
        <th width="10%" style="text-align:center;">详情</th>

</tr>
</table>
<div style="border:1px solid #ccc;" id="invInfo">
<table  cellpadding="0" cellspacing="0" class="detailsList" id="touziren" style="" >
           <tr>
               <td width="20%" style="text-align:center;">企业法人</td>
               <td width="20%" style="text-align:center;">顺丰速运有限公司</td>
               <td width="25%" style="text-align:center;"></td>
               <td width="25%" style="text-align:center;"></td>
               <td width="10%" style="text-align:center;">
                        <a href="#" onclick="return alert('该公司的股东及出资信息在2014年3月1日后发生变化的,股东详情企业自主公示');">详情</a>
                </td>
            </tr>
    </table>
        <table  cellpadding="0" cellspacing="0" class="detailsList">
            <tr><th colspan="6" style="text-align:right;">
                    <<&nbsp; &nbsp;
                1/1&nbsp;&nbsp;
                    >>
            </th></tr>
        </table>
</div>




          </br>
<table  cellpadding="0" cellspacing="0" class="detailsList">
    <tr width="95%"><th colspan="4" style="text-align:center;">变更信息</th></tr>
    <tr width="95%">
        <th width="15%" style="text-align:center;"> 变更事项</th>
        <th width="35%" style="text-align:center;"> 变更前内容</th>
        <th width="35%" style="text-align:center;"> 变更后内容</th>
        <th width="15%" style="text-align:center;"> 变更日期</th>
    </tr>
</table>
<div id="biangeng" style="border:1px solid #ccc;">
        <table  cellpadding="0" cellspacing="0" class="detailsList">
                        <tr width="95%">
                <td width="15%" style="text-align:center;">章程备案</td>
                <td width="35%" style="text-align:center;">章程备案(变更前)</td>
                <td width="35%" style="text-align:center;">准予章程备案</td>
                <td width="15%" style="text-align:center;">2016年05月10日</td>
            </tr>
            <tr width="95%">
                <td width="15%" style="text-align:center;">具体经营项目申报</td>
                <td width="35%" style="text-align:center;">国际货运代理;货物进出口（专营专控商品除外）;技术进出口;广告业;跨省快递业务;国际快递业务;道路货物运输;省内快递业务;</td>
                <td width="35%" style="text-align:center;">国际快递业务;跨省快递业务;省内快递业务;道路货物运输;国际货运代理;货物进出口（专营专控商品除外）;技术进出口;广告业;其他仓储业（不含原油、成品油仓储、燃气仓储、危险品仓储）;</td>
                <td width="15%" style="text-align:center;">2016年05月10日</td>
            </tr>
            <tr width="95%">
                <td width="15%" style="text-align:center;">换照</td>
                <td width="35%" style="text-align:center;">换照(变更前)</td>
                <td width="35%" style="text-align:center;">换照</td>
                <td width="15%" style="text-align:center;">2016年03月04日</td>
            </tr>
    <tr width="95%">
            <table  cellpadding="0" cellspacing="0" class="detailsList">
                <tr><th colspan="6" style="text-align:right;">
                        <<&nbsp;&nbsp;
                1/2&nbsp;&nbsp;
                        <a href="javascript:void(0);" style="text-decoration:none;" onclick="chaToPage('2','http://gsxt.gzaic.gov.cn/aiccips/','GSpublicity/entChaPage');">>></a>
                </th></tr>
            </table>
    </tr>
    </table>

</div>
           </br>
            </div>
		</div>
    </div>
    <br><br>
  </div>
﻿<div style="width:990px;height:55px;text-align:center;margin:0 auto; padding-top:20px;font-size:14px;text-align:center; color:#fff;">
    <div class="banqun">
            版权所有：广东省工商行政管理局&nbsp;&nbsp;
        <a href="http://gsxt.gdgs.gov.cn:81/aiceps/portal/consult.html" target="_blank"  style="color: red;"><u>全省工商业务咨询电话</u>&nbsp;</a>
        <br> 地址：广州市天河区体育西路57号&nbsp;&nbsp;邮政编码：510620 &nbsp;&nbsp; 建议使用IE8及以上版本浏览器
<script src="http://s4.cnzz.com/z_stat.php?id=1258472182&web_id=1258472182" language="JavaScript"></script>
    </div>

</div></body>
</html>
'''

en_guangdong_qyxx_nb = '''

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>企业信用信息公示系统</title>
    <link href="http://gsxt.gdgs.gov.cn/aiccips/css/public3.css" type="text/css" rel="stylesheet" />
    <link rel="stylesheet" type="text/css" href="http://gsxt.gdgs.gov.cn/aiccips/css/style.css"/>
    <script type="text/javascript">
        function retnCoinid(coinid){
            if(coinid != null){
                if("036".equals(coinid)){
                    coinid="澳大利亚元";
                }else if("040".equals(coinid)){
                    coinid="奥地利先令";
                }else if("056".equals(coinid)){
                    coinid="比利时法郎";
                }else if("124".equals(coinid)){
                    coinid="加元";
                }else if("156".equals(coinid)){
                    coinid="人民币";
                }else if("208".equals(coinid)){
                    coinid="丹麦克朗";
                }else if("250".equals(coinid)){
                    coinid="法国法郎";
                }else if("280".equals(coinid)){
                    coinid="德国马克";
                }else if("344".equals(coinid)){
                    coinid="香港元";
                }else if("392".equals(coinid)){
                    coinid="日元";
                }else if("446".equals(coinid)){
                    coinid="澳元";
                }else if("528".equals(coinid)){
                    coinid="荷兰盾";
                }else if("578".equals(coinid)){
                    coinid="挪威克朗";
                }else if("702".equals(coinid)){
                    coinid="瑞典克朗";
                }else if("752".equals(coinid)){
                    coinid="新加坡元";
                }else if("756".equals(coinid)){
                    coinid="瑞士法郎";
                }else if("826".equals(coinid)){
                    coinid="英镑";
                }else if("840".equals(coinid)){
                    coinid="美元";
                }else if("954".equals(coinid)){
                    coinid="欧元";
                }else if("n36".equals(coinid)){
                    coinid="澳大利亚元";
                }else {
                    coinid="人民币";
                }
             }
            return coinid;
        }
    </script>
</head>

<body >
<form id="topForm" action="" method="post">
<input type="hidden" id="aiccipsUrl" value="http://gsxt.gdgs.gov.cn/aiccips/">
<input type="hidden" id="entNo" name="entNo" value="">
<input type="hidden" id="entType" name="entType" value="">
<input type="hidden" id="regOrg" name="regOrg" value="">
</form>
<div style="display: none;">
<script type="text/javascript" src="http://gsxt.gdgs.gov.cn/aiccips/js/cnzz.js"></script>
</div>
<div id="header" style="background-image: url('http://gsxt.gdgs.gov.cn/aiccips//images/header_02_gd.png');width:990px;height:125px;">
        <div class="top-a">
            <a href="http://gsxt.saic.gov.cn/">全国首页</a>
            <a href="#" onclick="window.open('http://gsxt.gdgs.gov.cn/aiccips/')">地方局首页</a>
        </div>
</div>
<div id="details" class="clear">
    <div style="text-align: left;height: 35px">
        <h2>佛山市南湖国际旅行社有限责任公司&nbsp;&nbsp;&nbsp;&nbsp;统一社会信用代码：91440604776910212C</h2>
    </div>  <br>
    <div id="detailsCon" style="width: 100%">
    <table id="t01" cellspacing="0" cellpadding="0" class="detailsList">
    <tbody>
    <tr>
        <th style="text-align: center;color: red">
            2014年度年度报告 红色为修改过的信息项
         </th>

    </tr>
    <tr><th style="text-align: center;font-size: 14px;">企业基本信息</th>
    </tr>

    </tbody>
</table>
<table cellspacing="0" cellpadding="0" class="detailsList">
    <tbody>
    <tr>
        <th style="width: 20%"><span id="uniSCID" style="font-weight:bold; font-size: 14px;">统一社会信用代码</span></th>
        <td colspan="3">91440604776910212C</td>
    </tr>
    <tr>
        <th style="width: 20%"><span id="RegistNo" style="font-weight:bold; font-size: 14px;">注册号</span></th>
        <td style="width: 30%">440602000139697                     </td>
        <th style="width: 20%"><span id="EntName"  style="font-weight:bold;font-size: 14px; ">企业名称</span></th>
        <td style="width: 30%">佛山市南湖国际旅行社有限责任公司</td>
    </tr>
    <tr>
        <th><span id="EntPhone"  style="font-weight:bold;font-size: 14px; ">企业联系电话</span></th>
        <td>82320207</td>
        <th><span id="EntZip"  style="font-weight:bold;font-size: 14px; ">邮政编码</span></th>
        <td>528000</td>

    </tr>
    <tr>
        <th><span id="EntAddress"  style="font-weight:bold;font-size: 14px; ">企业通信地址</span></th>
        <td colspan="3">佛山市禅城区汾江中路侨苑新村二栋二楼之二</td>
    </tr>
    <tr>
        <th><span id="EntEmail"  style="font-weight:bold;font-size: 14px; ">电子邮箱</span></th>
        <td> </td>
        <th><span id="IsTransferStock"  style="font-weight:bold;font-size: 14px; ">有限责任公司本年度是否发生股东股权转让</span></th>
        <td>
                       否
        </td>
    </tr>
    <tr>
        <th><span id="EntState"  style="font-weight:bold; font-size: 14px;">企业经营状态</span></th>
        <td>
                开业
        </td>
        <th><span id="IsWeb"  style="font-weight:bold; font-size: 14px;">是否有网站或网店</span></th>
        <td>
                否
        </td>

    </tr>

    <tr>
        <th><span id="IsInveInfo"  style="font-weight:bold; font-size: 14px;">企业是否有对外投资设立企业信息</span></th>
        <td>
                否
        </td>

        <th><span id="EmpNumber"  style="font-weight:bold;font-size: 14px; ">从业人数</span></th>
                    <td>120人</td>


    </tr>
    </tbody>
    </table>
    <br>
<table id="t02" cellspacing="0" cellpadding="0" class="detailsList">
    <tbody>
</table>
<br>


<table id="t03" cellspacing="0" cellpadding="0" class="detailsList">
    <tbody>
    <tr>
        <th colspan="7" style="text-align: center"> <span id="NC" style="font-size: 14px; font-weight: bold;">股东及出资信息</span></th>
    </tr>

    <tr>
        <th style="text-align: center">股东</th>
        <th style="text-align: center">认缴出资额（万元）</th>
        <th style="text-align: center">认缴出资时间</th>
        <th style="text-align: center">认缴出资方式</th>
        <th style="text-align: center">实缴出资额（万元）</th>
        <th style="text-align: center">出资时间</th>
        <th style="text-align: center">出资方式</th>
    </tr>
        <tr>
            <td style="text-align: center">林露明</td>
            <td style="text-align: center">8.4万人民币元</td>
            <td style="text-align: center">
                     2015年03月21日</td>
            <td style="text-align: center">
                货币
            </td>
            <td style="text-align: center">8.4万人民币元</td>
                <td style="text-align: center">2015年03月21日</td>
            <td style="text-align: center">
                货币
            </td>
        </tr>
        <tr>
            <td style="text-align: center">广东南湖国际旅行社有限责任公司</td>
            <td style="text-align: center">21.6万人民币元</td>
            <td style="text-align: center">
                     2015年03月21日</td>
            <td style="text-align: center">
                货币
            </td>
            <td style="text-align: center">21.6万人民币元</td>
                <td style="text-align: center">2015年03月21日</td>
            <td style="text-align: center">
                货币
            </td>
        </tr>
</table>

<br>
<table id="t04" cellspacing="0" cellpadding="0" class="detailsList">
    <tbody>
    <tr>
        <th colspan="7" style="text-align: center"><span id="ND" style="font-size: 14px; font-weight: bold;">对外投资信息</span></th>
    </tr>

        <tr>
            <th colspan="4"  style="text-align: center;width: 55%">投资设立企业或购买股权企业名称</th>
            <th colspan="3" style="text-align: center">注册号</th>
        </tr>
        <tr>
            <td colspan="7" style="text-align: center">暂无数据</td>
        </tr>
</table>
<br>
<table id="t05" cellspacing="0" cellpadding="0" class="detailsList">
    <tr>
        <th colspan="6" style="text-align: center"> <span id="NE" style="font-size: 14px; font-weight: bold;">企业资产状况信息</span></th>
    </tr>
    <tbody>
        <tr>
            <th style="width: 20%"><span id="AssetsTotalAmount"  style="font-weight:bold; font-size: 14px;">资产总额</span></th>
                <input type="hidden" id="coinid" value="156"/>
                    <td style="width: 10%" colspan="2">企业选择不公示</td>
            <th style="width: 20%"><span id="LiabilitiesAmount"  style="font-weight:bold; font-size: 14px;">负债总额</span></th>
                    <td style="width: 10%" colspan="2">企业选择不公示</td>
        </tr>
        <tr>
            <th><span id="SalesAmount"  style="font-weight:bold; font-size: 14px;">营业总收入</span></th>
                    <td style="width: 10%" colspan="2">企业选择不公示</td>
            <th><span id="BusinessAmount"  style="font-weight:bold; font-size: 14px;">其中：主营业务收入</span></th>
                     <td style="width: 10%" colspan="2">企业选择不公示</td>
        </tr>
        <tr>
            <th><span id="ProfitsAmount"  style="font-weight:bold; font-size: 14px;">利润总额</span></th>
                    <td style="width: 10%" colspan="2">企业选择不公示</td>
            <th><span id="NetProfitAmount"  style="font-weight:bold; font-size: 14px;">净利润</span></th>
                    <td style="width: 10%" colspan="2">企业选择不公示</td>
        </tr>
        <tr>
            <th><span id="TaxAmount"  style="font-weight:bold; font-size: 14px;">纳税总额</span></th>
                    <td style="width: 10%" colspan="2">企业选择不公示</td>
            <th><span id="EquityAmount"  style="font-weight:bold; font-size: 14px;">所有者权益合计</span></th>
                    <td style="width: 10%" colspan="2">企业选择不公示</td>
        </tr>
    </tbody>
</table> <br>


    <table  cellpadding="0" cellspacing="0" class="detailsList">
        <tr><th colspan="8" style="text-align:center;"><span id="NI" style="font-size: 14px; font-weight: bold;">对外提供保证担保信息</span></th></tr>
        <tr width="95%">
            <th width="10%" height="40" style="text-align:center;">债权人</th>
            <th width="10%" style="text-align:center;">债务人</th>
            <th width="10%" style="text-align:center;">主债权种类</th>
            <th width="10%" style="text-align:center;">主债权数额</th>
            <th width="20%" style="text-align:center;">履行债务的期限</th>
            <th width="10%" style="text-align:center;">保证的期间</th>
            <th width="10%" style="text-align:center;">保证的方式</th>
            <th width="20%" style="text-align:center;">保证担保的范围</th>
        </tr>
            <tr>
                <td colspan="8" style="text-align: center">暂无数据</td>
            </tr>

      </table>
        <br>
        <!-- 纠错记录 -->
    <table  cellpadding="0" cellspacing="0" class="detailsList">
        <tr><th colspan="4" style="text-align:center"><span id="NL" style="font-size: 14px; font-weight: bold;">股权变更信息</span></th></tr>
        <tr width="95%">
            <th width="25%" style="text-align:center;">股东</th>
            <th width="25%" style="text-align:center;">变更前股权比例</th>
            <th width="25%" style="text-align:center;">变更后股权比例</th>
            <th width="25%" style="text-align:center;">股权变更日期</th>
        </tr>
     </table>
    <script type="text/javascript">
//        $(function(){
//            var coinid = $("#coinid").val();
//            var str_coinid = retnCoinid(coinid);
//            for(var i=0;i<8;i++){
//                document.getElementById("shar_"+i).innerHTML=str_coinid;
//            }
//        });
    </script>
<script type="text/javascript" src="http://gsxt.gdgs.gov.cn/aiccips//js/jquery.min.js"></script>
<script type="text/javascript">
    var listtrcorretion=[];
    for(var i=0;i<listtrcorretion.length;i++){

       if(listtrcorretion[i]['parentitem']=='NA'){
             var someone=listtrcorretion[i]['subitemcolumn'];
             $("#"+someone).css("color","red");
            continue;
       }
        if(listtrcorretion[i]['parentitem']=='NB'){
            $("#NB").css("color","red");
            continue;
        }
        if(listtrcorretion[i]['parentitem']=='NC'){
            $("#NC").css("color","red");
            continue;
        }
        if(listtrcorretion[i]['parentitem']=='ND'){
            $("#ND").css("color","red");
            continue;
        }
        if(listtrcorretion[i]['parentitem']=='NF'){
            $("#NF").css("color","red");
            var someone=listtrcorretion[i]['subitemcolumn'];
            $("#"+someone).css("color","red");
            continue;
        }
        if(listtrcorretion[i]['parentitem']=='NG'){
            $("#NG").css("color","red");
            var someone=listtrcorretion[i]['subitemcolumn'];
            $("#"+someone).css("color","red");

            continue;
        }
        if(listtrcorretion[i]['parentitem']=='NH'){
            $("#NH").css("color","red");
            continue;
        }
        if(listtrcorretion[i]['parentitem']=='NI'){
            $("#NI").css("color","red");
            continue;
        }
        if(listtrcorretion[i]['parentitem']=='NL'){
            $("#NL").css("color","red");
            continue;
        }
        if(listtrcorretion[i]['parentitem']=='NE'){
            $("#NE").css("color","red");
            var someone=listtrcorretion[i]['subitemcolumn'];
            $("#"+someone).css("color","red");
            continue;
        }
        if(listtrcorretion[i]['parentitem']=='NK'){
            $("#NK").css("color","red");
            continue;
        }
        if(listtrcorretion[i]['parentitem']=='NE_F'){
            $("#NE_F").css("color","red");
            var someone=listtrcorretion[i]['subitemcolumn'];
            $("#"+someone).css("color","red");
            continue;
        }
        if(listtrcorretion[i]['parentitem']=='NE_G'){
            $("#NE_G").css("color","red");
            var someone=listtrcorretion[i]['subitemcolumn'];
            $("#"+someone).css("color","red");
            continue;
        }

    }

</script>
<br>
    <table width="99%" cellspacing="0" cellpadding="0" class="detailsList" id="table_1NA">
        <tr >
            <th colspan="5" height="40" style="text-align: center">修改记录</th>
        </tr>
        <tr >
            <th width="5%" height="40" style="text-align: center">序号</th>
            <th width="15%" height="40" style="text-align: center">修改事项</th>
            <th width="30%" height="40" style="text-align: center">修改前</th>
            <th width="30%" height="40" style="text-align: center">修改后</th>
            <th width="20%" height="40" style="text-align: center">修改日期</th>
        </tr>
        <tr >
            <td colspan="5" height="42" style="text-align: center" >暂无数据</td>
        </tr>
    </table>








    </div>

</div>
<div style="width:990px;height:55px;text-align:center;margin:0 auto; padding-top:20px;font-size:14px;text-align:center; color:#fff;">
    <div class="banqun">
            版权所有：广东省工商行政管理局&nbsp;&nbsp;
        <a href="http://gsxt.gdgs.gov.cn:81/aiceps/portal/consult.html" target="_blank"  style="color: red;"><u>全省工商业务咨询电话</u>&nbsp;</a>
        <br> 地址：广州市天河区体育西路57号&nbsp;&nbsp;邮政编码：510620 &nbsp;&nbsp; 建议使用IE8及以上版本浏览器

    </div>
</div></body>
</html>
'''

en_beijing_xzcf = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet" />
	<link href="/country_credit/bj/css/style.css" type="text/css" rel="stylesheet" />
	<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script>
	<script type="text/javascript">
	   function jumppage(pageNo){
	      $("#pageNo").val(pageNo);
	      $("#xzcfForm").submit();
	   }
	</script>
</head>

<body>
<div style="height:auto;">
	  <div id="xzcf">
	      <form action='/gsgs/gsxzcfAction!list.dhtml?entId=B0B7988F4AA7483EB70CA87018D95F08' method="post" id="xzcfForm">
			<table  cellpadding="0" cellspacing="0" class="detailsList">
					<tr width="95%"><th colspan="7" style="text-align:center;">行政处罚信息</th></tr>
					<tr width="95%">
						<th width="5%"style="text-align:center;">序号</th>
						<th width="10%"style="text-align:center;">行政处罚<br>决定书文号</th>
						<th width="20%"style="text-align:center;">违法行为类型</th>
						<th width="10%"style="text-align:center;">行政处罚内容</th>
						<th width="10%"style="text-align:center;">作出行政处罚<br>决定机关名称</th>
						<th width="10%"style="text-align:center;">作出行政处罚<br>决定日期</th>
						<th width="10%"style="text-align:center;">详情</th>
					</tr>



							<tr width="95%">
								<td style="text-align:center;">1</td>
								<td style="text-align:left;">京工商海处字〔2016〕第77号</td>
								<td style="text-align:left;"></td>
								<td style="text-align:left;">罚款1988.01元。</td>
								<td style="text-align:left;">北京市工商行政管理局海淀分局</td>
								<td style="text-align:center;">2016年02月16日</td>
		                        <td style="text-align:left;"><a href="/gsgs/gsxzcfAction!detail.dhtml?cid=N0000000000000100000000702687811" target="_blank">详情</a></td>
							</tr>


				<tr>
				 <th colspan="7" style="text-align:rigth;"><a href="javascript:void(0)" title="上一页" style="vertical-align:bottom" onclick="jumppage('0');return false"><<</a>&nbsp;&nbsp;<font style='text-decoration:none;color:red'>1</font>&nbsp;&nbsp;<a href="javascript:void(0)" title="下一页" style="vertical-align:bottom"  onclick="jumppage('2');return false">>></a>&nbsp;&nbsp;<input type="hidden" id="pageNo" name="pageNo" value='1' /><input type="hidden" value='1' id="pagescount"/><input type="hidden" id="pageSize" name="pageSize"  value='10' /><input type="hidden" id="clear" name="clear" /></th>
				</tr>
				</table>
			 </form>
  </div>
</div>
</body>
</html>
'''

en_bj_dengjijiguan='''





<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet" />
	<link href="/country_credit/bj/css/style.css" type="text/css" rel="stylesheet" />
	<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script><!-- 1.9版本jQuery js   9-->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/pubInfo.js"></script><!-- 北京首页pubInfo.js js   -->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/gs_tab.js"></script><!-- 工商公示 tab页签的变化 js   -->
	<script type="text/javascript">
	var rootPath = '';
 	var entId = '20e38b8c4a53cc81014a5c7e58fa5cec';
	var entName = '博湃（北京）汽车技术服务有限公司';
	var entNo = '110000450275141';
	var type = '';
	var checkCodeServletName = "CheckCodeCaptcha";
	$(document).ready(function(){
	    if(!type){
		    gsCheckCurrentTab('djxxDiv',entId);
		}else{
		    gsCheckCurrentTab(type,entId);
		}
	});

//工商公示 页面显示tab也内容显示
function gsCheckCurrentTab(currentId,entId){
	var liAIdArr =['djxxDiv','bgxxDiv','dcdyDiv','gqczdjDiv','xzcfDiv','jyycDiv','yzwfDiv','ccycDiv'];
	for(var i=0;i<liAIdArr.length;i++){
		if(currentId==liAIdArr[i]){
			$("#"+currentId).css('display','block');
			if(currentId=='djxxDiv'){//登记信息
				var entName = encodeURIComponent(jQuery.trim(entName));
				$("#tzrFrame").attr("src",rootPath+"/gjjbj/gjjQueryCreditAction!tzrFrame.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entId))+"&entName="+entName+"&clear=true&timeStamp="+new Date().getTime());
				$("#bgxxFrame").attr("src",rootPath+"/gjjbj/gjjQueryCreditAction!biangengFrame.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='bgxxDiv'){//变更信息
				$("#zyryFrame").attr("src",rootPath+"/gjjbj/gjjQueryCreditAction!zyryFrame.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
				$("#fzjgFrame").attr("src",rootPath+"/gjjbj/gjjQueryCreditAction!fzjgFrame.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entName))+"&clear=true&timeStamp="+new Date().getTime());
				ajaxChange(entId);
			}else if(currentId=='dcdyDiv'){//动产抵押
				$("#dcdyFrame").attr("src",rootPath+"/gjjbjTab/gjjTabQueryCreditAction!dcdyFrame.dhtml?entId="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='gqczdjDiv'){//股权出质登记信息
				 $("#gqczdjFrame").attr("src",rootPath+"/gdczdj/gdczdjAction!gdczdjFrame.dhtml?entId="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='xzcfDiv'){//行政处罚
				$("#xzcfFrame").attr("src",rootPath+"/gsgs/gsxzcfAction!list.dhtml?entId="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='jyycDiv'){//经营异常
				$("#jyycFrame").attr("src",rootPath+"/gsgs/gsxzcfAction!list_jyycxx.dhtml?entId="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='yzwfDiv'){//严重违法
				$("#yzwfFrame").attr("src",rootPath+"/gsgs/gsxzcfAction!list_yzwfxx.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}else if(currentId=='ccycDiv'){//抽查检查
				$("#ccycFrame").attr("src",rootPath+"/gsgs/gsxzcfAction!list_ccjcxx.dhtml?ent_id="+encodeURIComponent(jQuery.trim(entId))+"&clear=true&timeStamp="+new Date().getTime());
			}
		}else{
			$("#"+liAIdArr[i]).css('display','none');
		}
	}
}
	</script>
</head>
<body>
<div id="header">
	<div class="top">
		<div class="top-a">
			<a href="#"  onclick="toCountryIndex();">全国首页</a>
			<a href="#" onclick="toIndex();">地方局首页</a>
		 </div> <!-- 新的tab头 -->
	</div>
</div>
<div id="details" class="clear">

		<h2>

  		 博湃（北京）汽车技术服务有限公司 &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;

  		  	注册号：110000450275141

  		 &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;

   </h2><br/>
   <div id="leftTabs">
	    <ul>
	      <li class="current" style="margin-bottom:2px;"><p>工<br />商<br />公<br />示<br />信<br />息</p></li>
		<li onclick="togo('2','215A78CBC2B3706CF43C3658E2BC9688')" style="margin-bottom:2px;"><p>企<br />业<br />公<br />示<br />信<br />息</p></li>
	     <li onclick="togo('3','215A78CBC2B3706CF43C3658E2BC9688')"><p style="padding-top:15px;">其<br />他<br />部<br />门<br />公<br />示<br />信<br />息</p></li>
	    </ul>
   </div>

   	<div id="detailsCon" style="min-height:800px;height:auto;">
   		<div class="dConBox" >
   			  <div class="tabs" id="tabs">
			       <ul>
							<li id="0" class="current" onclick="gsCheckCurrentTab('djxxDiv','20e38b8c4a53cc81014a5c7e58fa5cec'),changeStyle('tabs',this)">登记信息</li>
							<li id="1" onclick="gsCheckCurrentTab('bgxxDiv','20e38b8c4a53cc81014a5c7e58fa5cec'),changeStyle('tabs',this)">备案信息</li>
					       	<li id="2" onclick="gsCheckCurrentTab('dcdyDiv','20e38b8c4a53cc81014a5c7e58fa5cec'),changeStyle('tabs',this)">动产抵押登记信息</li>
							<li id="3" onclick="gsCheckCurrentTab('gqczdjDiv','20e38b8c4a53cc81014a5c7e58fa5cec'),changeStyle('tabs',this)">股权出质登记信息</li>
							<li id="4" onclick="gsCheckCurrentTab('xzcfDiv','20e38b8c4a53cc81014a5c7e58fa5cec'),changeStyle('tabs',this)">行政处罚信息</li>
							<li id="5"  onclick="gsCheckCurrentTab('jyycDiv','20e38b8c4a53cc81014a5c7e58fa5cec'),changeStyle('tabs',this)">经营异常信息</li>
							<li id="6"  onclick="gsCheckCurrentTab('yzwfDiv','20e38b8c4a53cc81014a5c7e58fa5cec'),changeStyle('tabs',this)">严重违法信息</li>
							<li id="7"  onclick="gsCheckCurrentTab('ccycDiv','20e38b8c4a53cc81014a5c7e58fa5cec'),changeStyle('tabs',this)">抽查检查信息</li>
						 </ul>
		      </div>
		      <br/>
		      <!-- 登记信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
		       <div id="djxxDiv">
			      <div id="jbxx">


						<!-- 内资公司法人 -->





<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet" />
</head>
<body>
	 <table cellspacing="0" cellpadding="0" class="detailsList" >
	      	<tr>
	      		<th colspan="4" style="text-align:center;">基本信息 </th>
	      	</tr>
	        <tr>

		        <th width="20%">注册号</th>
	         	<td width="30%">110000450275141</td>

	          <th>名称</th>
	          <td width="30%">博湃（北京）汽车技术服务有限公司</td>
	        </tr>
	        <tr>
		        <th>类型</th>
		        <td>有限责任公司(台港澳法人独资)</td>
		        <th width="20%">法定代表人</th>
		        <td>吉伟</td>
	        </tr>
	         <tr>
		        <th>注册资本</th>
		        <td>

			      	   600 万元 美元

			        </td>
		        <th width="20%">成立日期</th>
		        <td>2014年12月18日</td>
	        </tr>
	        <tr>
	           <th>住所</th>
	           <td colspan="3">北京市海淀区万寿路西街2号4层031室</td>
	        </tr>
	         <tr>
	        	<th>营业期限自</th>
	            <td>2014年12月18日</td>
	         	 <th>营业期限至</th>
	           <td>2044年12月17日</td>
	        </tr>
	         <tr>
	          <th>经营范围</th>
	         <td colspan="3">汽车应用软件技术开发、技术服务、技术咨询、技术转让、技术培训；销售自行开发的软件产品；批发汽车零配件、仪器仪表。（依法须经批准的项目，经相关部门批准后依批准的内容开展经营活动。）</td>
	        </tr>
	         <tr>
	          <th width="20%">登记机关</th>
	          <td width="30%">

			    	   北京市工商行政管理局（<span style="color:red;">登记业务及档案查询在所在地工商分局办理。</span>）

	          </td>
	         <th width="20%">核准日期</th>
	          	<td width="30%">2015年05月26日</td>
	        </tr>
	         <tr>
	        	<th>登记状态</th>
		        <td>在营（开业）企业</td>

        	          <th width="20%"></th>
      	              <td></td>

	        </tr>
	   </table>
</body>
</html>

			      </div><br/>
			      <div id="tzr">
			      		<iframe id="tzrFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div><br/>
			      <div id="bgxx">
			      		<iframe id="bgxxFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
		      </div>
		       <!-- 变更信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
		      <div id="bgxxDiv"  style="display:none">
			      <div id="zyry">
			      		<iframe id="zyryFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div><br/>
				  <div id="fzjg">
				  		<iframe id="fzjgFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
				  </div><br/>
				  <div id="qsxx">
				  </div>
			  </div>
			   <!-- 动产抵押登记信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
			   <div id="dcdyDiv"  style="display:none">
			      <div id="dcdy">
			      		<iframe id="dcdyFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>
			   <!-- 股权出质登记信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
			   <div id="gqczdjDiv"  style="display:none">
			      <div id="gqczdj">
			      		<iframe id="gqczdjFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>
			   <!-- 行政处罚信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
			  <div id="xzcfDiv"  style="display:none">
			      <div id="xzcf">
			      		<iframe id="xzcfFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>
			   <!-- 经营异常信息 ~~~~~~~~~~~begin~~~~~~~~~ -->
			  <div id="jyycDiv"  style="display:none">
			      <div id="jyyc">
			      		<iframe id="jyycFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>
			   <!-- 严重违法信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
			  <div id="yzwfDiv"  style="display:none">
			      <div id="yzwf">
			      		<iframe id="yzwfFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>
			   <!-- 抽查检查信息  ~~~~~~~~~~~begin~~~~~~~~~ -->
			  <div id="ccycDiv"  style="display:none">
			      <div id="ccyc">
			      		<iframe id="ccycFrame" scrolling="yes"  onload="Javascript:SetCwinHeight(this)"  frameborder="0" src="" style="width:100%;"></iframe>
			      </div>
			  </div>

  		 </div>
  	</div>
<div class="banqun" style="padding-bottom:20px;margin-top:10px;">
              版权所有：北京市工商行政管理局&nbsp;&nbsp;&nbsp;&nbsp;地址：北京市海淀区苏州街36号&nbsp;&nbsp;&nbsp;&nbsp;邮政编码：100080<br />
              <!-- 业务咨询电话：010-82691213，010-82691523&nbsp;&nbsp;&nbsp;&nbsp;技术支持电话：010-82691768（公示），010-82691101（年报） -->
</div>
<div style="display:none;">
<script src="http://s4.cnzz.com/z_stat.php?id=1257386840&web_id=1257386840" language="JavaScript"></script>
</div>
  </div>
</body>
</html>
'''

en_bj_bgxx = '''





<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet" />
	<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script><!-- 1.9版本jQuery js   -->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/pubInfo.js"></script><!-- 北京首页pubInfo.js js   -->
	<script type="text/javascript" src="/js/ajax/http.js" ></script>
	<script type="text/javascript">
	var rootPath = '';
 	var entId = 'A41C20985B4F40D19001D653EDCC4E95';
	var entName = '北京我爱我家房地产经纪有限公司';
	var entNo = '';
	</script>
	<style>
	html { overflow:hidden; }
	</style>
</head>
<body>
	<form action="gjjbj/gjjQueryCreditAction!biangengFrame.dhtml" method="post"  name="iframeFrame" id="iframeFrame">
	<input type="hidden" id="pageNos" name="pageNos" value="1" />
	<input type="hidden" id="ent_id" name="ent_id" value="A41C20985B4F40D19001D653EDCC4E95"/>
	<table cellspacing="0" cellpadding="0" class="detailsList"  id="touziren" >
		<tbody id="table2">
			<tr width="95%"><th colspan="4" style="text-align:center;">变更信息</th></tr>
			<tr width="95%">
			<th width="15%" style="text-align:center;"> 变更事项</th>
			<th width="25%" style="text-align:center;"> 变更前内容</th>
			<th width="25%" style="text-align:center;"> 变更后内容</th>
			<th width="10%" style="text-align:center;"> 变更日期</th>
			</tr>



	         <tr id="tr1">
	         	<td>投资人</td>

		         	<td colspan='2'><a href="javascript:void(0);" onclick="showDialog('/gjjbj/gjjQueryCreditAction!tzrBgxx.dhtml?old_reg_his_id=20e38b8b50b3231a0150b778cfd16245&new_reg_his_id=20e38b8b51575c380151579dd6046847&clear=true&chr_id=null', '投资人信息详细', '468px');">详细</a></td>

	         	<td>2015-11-30</td>
	         </tr>

	         <tr id="tr1">
	         	<td>投资人</td>

		         	<td colspan='2'><a href="javascript:void(0);" onclick="showDialog('/gjjbj/gjjQueryCreditAction!tzrBgxx.dhtml?old_reg_his_id=20e38b8c5013b4a801501722e7dd7846&new_reg_his_id=20e38b8b50b3231a0150b778cfd16245&clear=true&chr_id=null', '投资人信息详细', '468px');">详细</a></td>

	         	<td>2015-10-30</td>
	         </tr>

	         <tr id="tr1">
	         	<td>投资人</td>

		         	<td colspan='2'><a href="javascript:void(0);" onclick="showDialog('/gjjbj/gjjQueryCreditAction!tzrBgxx.dhtml?old_reg_his_id=20e38b8c4b3a7c99014b4e21e1b1773f&new_reg_his_id=20e38b8c5013b4a801501722e7dd7846&clear=true&chr_id=null', '投资人信息详细', '468px');">详细</a></td>

	         	<td>2015-09-29</td>
	         </tr>

	         <tr id="tr1">
	         	<td>投资人</td>

		         	<td colspan='2'><a href="javascript:void(0);" onclick="showDialog('/gjjbj/gjjQueryCreditAction!tzrBgxx.dhtml?old_reg_his_id=a1a1a1a02e23b215012e26eb307541ec&new_reg_his_id=20e38b8c4b3a7c99014b4e21e1b1773f&clear=true&chr_id=null', '投资人信息详细', '468px');">详细</a></td>

	         	<td>2015-03-18</td>
	         </tr>

	         <tr id="tr1">
	         	<td>董事（理事）、经理、监事</td>

		         	<td colspan='2'><a href="javascript:void(0);" onclick="showDialog('/gjjbj/gjjQueryCreditAction!zyryBgxx.dhtml?old_reg_his_id=a1a1a1a02151fb48012152889cb04337&new_reg_his_id=20e38b8b45fa5521014603221cb15882&clear=true&chr_id=null', '投资人信息详细', '468px');">详细</a></td>

	         	<td>2014-05-22</td>
	         </tr>






				<tr>
					<th colspan='4' style="text-align:right;">
					<a href="javascript:void(0)" title="上一页" style="vertical-align:bottom" onclick="jumppage('0');return false"><<</a>&nbsp;&nbsp;<a href="javascript:void(0)" onclick="jumppage('1');return false"><font style='text-decoration:none;color:red'>1</font></a>&nbsp;&nbsp;<a href="javascript:void(0)" title="下一页" style="vertical-align:bottom"  onclick="jumppage('2');return false">>></a>&nbsp;&nbsp;<input type="hidden" id="pageNo" name="pageNo" value='1' /><input type="hidden" value='1' id="pagescount"/><input type="hidden" id="pageSize" name="pageSize"  value='5' /><input type="hidden" id="clear" name="clear" />
				</th>
				</tr>

		</tbody>
	</table>
   </form>
</body>
</html>
'''

en_beijing_bugfix = '''





<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>全国市场主体信用信息公示系统</title>
	<link href="/country_credit/bj/css/public3.css" type="text/css" rel="stylesheet" />
	<script type="text/javascript" src="/country_credit/bj/javascript/jquery-1.9.1.js"></script><!-- 1.9版本jQuery js   -->
	<script type="text/javascript" src="/country_credit/bj/javascript/bj_js/pubInfo.js"></script><!-- 北京首页pubInfo.js js   -->
	<script type="text/javascript">
	var rootPath = '';
 	var entId = 'a1a1a1a02a1dfb52012a59b342f80676';
	var entName = '';
	var entNo = '';

	function viewInfo(entId){
		var inv = encodeURIComponent(jQuery.trim(entId));
		var entName = encodeURIComponent(jQuery.trim(entName));
		var url = rootPath + "/gjjbj/gjjQueryCreditAction!touzirenInfo.dhtml?chr_id="+inv+"&entName="+entName+"&timeStamp="+new Date().getTime()+"&fqr=";//给该url一个时间戳~~这样就必须每次从服务器读取数据;
		window.open(url);
	}
	</script>
	<style>
	html { overflow:hidden; }
	</style>
</head>
<body>
	<form action="gjjbj/gjjQueryCreditAction!tzrFrame.dhtml" method="post"  name="iframeFrame" id="iframeFrame">
	<input type="hidden" id="pageNos" name="pageNos" value="1" />
	<input type="hidden" id="ent_id" name="ent_id" value="a1a1a1a02a1dfb52012a59b342f80676"/>
	<input type="hidden" id="fqr" name="fqr" value=""/>
	<table cellspacing="0" cellpadding="0" class="detailsList"  id="touziren" >



					<tr>
						<th colspan="4" style="text-align:center;">


								股东信息</br>
								<span style="font-size:12px;">股东的出资信息截止2014年2月28日。2014年2月28日之后工商只公示股东姓名，其他出资信息由企业自行公示。</span>

						 </th>
					</tr>






		<tbody id="table2">
			<tr width="95%">


	          <th width="10%" style="text-align:center;">股东类型</th>
	          <th width="10%" style="text-align:center;">股东</th>

			  <th width="10%" style="text-align:center;">证照/证件类型</th>
			  <th width="10%" style="text-align:center;">证照/证件号码</th>



	        </tr>

	         <tr id="tr1">
	         	<td>自然人股东</td>
	         	<td>商建民</td>
	         	<td></td>
	         	<td></td>



	         </tr>

	         <tr id="tr1">
	         	<td>自然人股东</td>
	         	<td>王莉娟</td>
	         	<td></td>
	         	<td></td>



	         </tr>






						<tr><th colspan='4' style='text-align:right;'><a href="javascript:void(0)" title="上一页" style="vertical-align:bottom" onclick="jumppage('0');return false"><<</a>&nbsp;&nbsp;<font style='text-decoration:none;color:red'>1</font>&nbsp;&nbsp;<a href="javascript:void(0)" title="下一页" style="vertical-align:bottom"  onclick="jumppage('2');return false">>></a>&nbsp;&nbsp;<input type="hidden" id="pageNo" name="pageNo" value='1' /><input type="hidden" value='1' id="pagescount"/><input type="hidden" id="pageSize" name="pageSize"  value='5' /><input type="hidden" id="clear" name="clear" /></th></tr>






		</tbody>
	</table>
   </form>
</body>
</html>
'''