executeOnServer=function(model,url,callback){return $.ajax({url:url,type:'POST',data:JSON.stringify(model),dataType:"json",contentType:"application/json; charset=utf-8",success:function(data){if(callback)
callback(data);else{if(data.redirect){location.href=resolveUrl(data.url);}}},error:function(error){alert("There was an error posting the data to the server: "+(error.responseText||error.statusText));}});};function getCookie(name){var matches=document.cookie.match(new RegExp("(?:^|; )"+name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g,'\\$1')+"=([^;]*)"));return matches?decodeURIComponent(matches[1]):undefined;}
function setCookie(name,value,options){options=options||{};var expires=options.expires;if(typeof expires=="number"&&expires){var d=new Date();d.setTime(d.getTime()+expires*1000);expires=options.expires=d;}
if(expires&&expires.toUTCString){options.expires=expires.toUTCString();}
value=encodeURIComponent(value);var updatedCookie=name+"="+value;for(var propName in options){updatedCookie+="; "+propName;var propValue=options[propName];if(propValue!==true){updatedCookie+="="+propValue;}}
document.cookie=updatedCookie;}
function bakeCookie(name,value){var cookie=[name,'=',JSON.stringify(value),'; domain=.',window.location.host.toString(),'; path=/;'].join('');setCookie(name,cookie);}
function readCookie(name){var cookie=getCookie(name);if(!cookie)
return undefined;var result=cookie.match(new RegExp(name+'=([^;]+)'));result&&(result=JSON.parse(result[1]));return result;}
function deleteCookie(name){document.cookie=[name,'=; expires=Thu, 01-Jan-1970 00:00:01 GMT; path=/; domain=.',window.location.host.toString()].join('');}
function getQueryVariable(variable){var query=window.location.search.substring(1);var vars=query.split('&');for(var i=0;i<vars.length;i++){var pair=vars[i].split('=');if(decodeURIComponent(pair[0])==variable){return decodeURIComponent(pair[1]);}}
console.log('Query variable %s not found',variable);}
function InitPopovers(){$('[data-toggle="tooltip"]').popover();}
var default_rest_options={is_show_error_message:true,cbFinally:undefined};function Delete(url,success,fail,options){var data={'justification':''};var contentType='';if(options.justification){data.justification=options.justification;contentType='application/json';}
$.ajax({url:url,type:'Delete',dataType:'json',contentType:contentType,data:JSON.stringify(data)}).done(function(data){_Success(success,data,options);}).fail(function(error){_Fail(fail,error,options);});}
function Get(url,success,fail,options){$.ajax({url:url,type:'GET',dataType:'json'}).done(function(data){_Success(success,data,options);}).fail(function(error){_Fail(fail,error,options);});}
function Post(url,data,success,fail,options){$.ajax({url:url,type:'POST',dataType:'json',contentType:'application/json',data:JSON.stringify(data)}).done(function(data){_Success(success,data,options);}).fail(function(error){_Fail(fail,error,options);});}
function Patch(url,data,success,fail,options){$.ajax({url:url,type:'PATCH',contentType:'application/json',dataType:'json',data:JSON.stringify(data)}).done(function(data){_Success(success,data,options);}).fail(function(error){_Fail(fail,error,options);});}
function _Success(cb,data,options){options=_.defaults({},default_rest_options,options);if(cb){cb(data);}
if(options.cbFinally)
options.cbFinally();}
function _Fail(cb,error,options){options=_.defaults({},default_rest_options,options);if(cb){cb(error);}
else{if(error.responseJSON&&error.responseJSON.message&&(typeof error.responseJSON.message)=='string'&&options.is_show_error_message){if(error.responseJSON.status){if(error.responseJSON.status==401){toastr.error('Необходима авторизация <a href="/logout/" style="color: yellow">Сменить пользователя<i class="icon sign out"></i> </a>');}
if(error.responseJSON.status==403){toastr.error('Не хватает прав для выполнения действия <a href="/logout/" style="color: yellow">Сменить пользователя<i class="icon sign out"></i> </a>');}}
else{toastr.error(error.responseJSON.message);}}
else{if(options.is_show_error_message){toastr.error('При обращении к API произошла ошибка');}}}
if(options.cbFinally)
options.cbFinally();}
var RestAPI=(function(){var self={};self.resource_url="";self.list=function(success,error,cbFinally){Get(self.resource_url,success,error,{cbFinally:cbFinally});};self.get=function(id,success,error,cbFinally){Get(self.resource_url+'/'+id,success,error,{cbFinally:cbFinally});};self.create=function(data,success,error,cbFinally){Post(self.resource_url,data,success,error,{cbFinally:cbFinally})};self.save=function(id,data,success,error,cbFinally){Patch(self.resource_url+'/'+id,data,success,error,{cbFinally:cbFinally});};self.delete=function(success,error,cbFinally){Delete(self.resource_url,success,error,{cbFinally:cbFinally})};return self;});function loader_show(){$('body').append('<div class="ui active dimmer"><div class="ui loader"></div></div>');}
function loader_close(){$('.ui.active.dimmer').removeClass('active');}