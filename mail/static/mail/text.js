// window.onload = function() {
//   var txts = document.getElementsByTagName('TEXTAREA');
//
//   for(var i = 0, l = txts.length; i < l; i++) {
//     if(/^[0-9]+$/.test(txts[i].getAttribute("maxlength"))) {
//       var func = function() {
//         var len = parseInt(this.getAttribute("maxlength"), 10);
//
//         if(this.value.length > len) {
//           alert('Maximum length exceeded: ' + len);
//           this.value = this.value.substr(0, len);
//           return false;
//         }
//       }
//
//       txts[i].onkeyup = func;
//       txts[i].onblur = func;
//     }
//   };
//
// }

window.onload = function() {
    var textbox = document.getElementById('id_content');
    var check_for_mustache_elements = function() {
        var html = '';
        var mustache_regex = /\{\{((?!\}\})(.|\n))*\}\}/g;
        var inner_regex = /[\w\.]+/;
        var found = textbox.value.match(mustache_regex);
        if (found) {
            for (var i = 0 ; i < found.length; i++) {
                // console.log(found[i].match(inner_regex)[0]);
                html += '<tr><td>';
                html += found[i].match(inner_regex)[0];
                html += '</td></tr>';
            }
        }
        document.getElementById('found_elements').innerHTML = html;
    }

    textbox.onkeyup = check_for_mustache_elements;
    textbox.onblur = check_for_mustache_elements;
}
