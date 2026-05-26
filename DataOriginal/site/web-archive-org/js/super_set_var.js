var _____WB$wombat$assign$function_____=function(name){return (self._wb_wombat && self._wb_wombat.local_init && self._wb_wombat.local_init(name))||self[name];};if(!self.__WB_pmw){self.__WB_pmw=function(obj){this.__WB_source=obj;return this;}}{
let window = _____WB$wombat$assign$function_____("window");
let self = _____WB$wombat$assign$function_____("self");
let document = _____WB$wombat$assign$function_____("document");
let location = _____WB$wombat$assign$function_____("location");
let top = _____WB$wombat$assign$function_____("top");
let parent = _____WB$wombat$assign$function_____("parent");
let frames = _____WB$wombat$assign$function_____("frames");
let opens = _____WB$wombat$assign$function_____("opens");
// "standard" read cookie function  (copied from Prusak's gwo_write.js)
function read_cookie(cookie_name) {
  var my_cookie=""+document.cookie;
  var ind=my_cookie.indexOf(cookie_name);
  if (ind==-1 || cookie_name=="") return ""; 
  var ind1=my_cookie.indexOf(';',ind);
  if (ind1==-1) ind1=my_cookie.length; 
  return unescape(my_cookie.substring(ind+cookie_name.length+1,ind1));
}

function superSetVar(appendValue,act,UA) { //act 0=append 1=overwrite 2=preserve
  var getVar = read_cookie('__utmv');       // lê o cookie __utmv
  hasValue = getVar.indexOf(appendValue);   // o cookie já tem o valor que se quer adicionar?
  removePrefix = /^.*\.(.*)/.exec(getVar);  // __utmv cookie tem o formato 12345678.cookieValue - remove o prefixo ##
  if (removePrefix && removePrefix[1]) { // se o cookie possui algum valor
    if (act==2){return;} //preservar, então sai
    if (act==1){newVar=appendValue;} //substituir o valor
    if (act==0){ //concatenar
      if (hasValue==-1) { //só concatena se o valor ainda não está no cookie
        newVar = removePrefix[1] + appendValue; // concatena o valor
      }
    }
  }else{ //se o cookie não possui qualquer valor, então atribui o valor passado
    newVar = appendValue;
  }
  var superSetVarTracker = _gat._getTracker(UA);  // define o tracker para chamar o _setVar
  superSetVarTracker._initData();  
  superSetVarTracker._setVar(newVar);                   // define o _setVar com o novo valor
}

function unSetVar(removeValue,UA){
  var getVar = read_cookie('__utmv');         // lê o cookie __utmv
  hasValue = getVar.indexOf(removeValue);     // o cookie tem o valor que se quer remover?
  if ( hasValue != -1 ) {                     // se o valor está no cookie então . . .  caso contrário, não há nada a ser feito.
    removePrefix = /^.*\.(.*)/.exec(getVar);  // __utmv cookie tem o formato 12345678.cookieValue - remove o prefixo ##
    if (removePrefix && removePrefix[1]) {    // se nós removemos o prefixo então. . .
      //
      var re = removeValue + '[^/]*';
      re = new RegExp(re,'g');
      newVar = removePrefix[1].replace(re,""); // newVar = removePrefix[1] MINUS removeValue
      //
      var superSetVarTracker = _gat._getTracker(UA);  // defina o tracker para chamar o _setVar
      superSetVarTracker._initData();  
      superSetVarTracker._setVar(newVar);                   // define o _setVar com o novo valor
    }
    
  }
}
}

/*
     FILE ARCHIVED ON 15:28:18 Jan 21, 2022 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 04:57:33 May 25, 2026.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  capture_cache.get: 0.555
  captures_list: 0.768
  exclusion.robots: 0.065
  exclusion.robots.policy: 0.052
  esindex: 0.011
  cdx.remote: 13.839
  LoadShardBlock: 81.64 (3)
  PetaboxLoader3.datanode: 132.686 (5)
  PetaboxLoader3.resolve: 81.498 (2)
  load_resource: 170.466
  loaddict: 45.839
*/