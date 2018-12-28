window.onload = function() {
    var textbox = document.getElementById('id_content');
    var check_for_mustache_elements = function() {
        var html = '';
        var mustache_regex = /\{\{((?!\}\})(.|\n))*\}\}/g;
        var inner_regex = /[\w\.]+/;
        var found = textbox.value.match(mustache_regex);
        if (found) {
            for (var i = 0 ; i < found.length; i++) {
                var element = found[i].match(inner_regex)[0];
                html += '<tr><td>';
                html += headers.includes(element) ? '' : '<b>';
                html += element;
                html += headers.includes(element) ? '' : '</b>';
                html += '</td></tr>';
            }
        }
        update_preview(found);
        document.getElementById('content_found').innerHTML = html;
    }
    var update_preview = function(found) {
        var html = textbox.value;
        var mismatch = document.getElementById('mismatch');
        var preview = document.getElementById('preview');
        for (var i = 0; i < headers.length; i++) {
            html = html.replace('{{' + headers[i] + '}}', first_row[i]);
        }
        html = html.replace(/\r\n|\n/g, '<br />');
        if (found && !found.every(function (element) { return headers.includes(element.replace(/{|}/g, '')); })) {
            mismatch.style.display = 'block';
            mismatch.innerHTML = 'You\'re missing the following: '
                + found
                    .filter(function (x) { return !headers.includes(x.replace(/{|}/g, '')); })
                    .join(', ')
                    .replace(/{|}/g, '');
        } else {
            mismatch.style.display = 'none';
        }

        if (html) {
            preview.style.display = 'block';
        } else {
            preview.style.display = 'none';
        }
        preview.innerHTML = html;
    }

    textbox.onkeyup = check_for_mustache_elements;
    textbox.onblur = check_for_mustache_elements;

    var fileInput = document.getElementById('id_send_list');
    var headers = [];
    var first_row = [];
    var load_handler = function(event) {
        var html = '';
        var csv = event.target.result;
        headers = csv.split(/\r\n|\n/)[0].split(',');
        first_row = csv.split(/\r\n|\n/)[1].split(',');
        for (var i = 0; i < headers.length; i++) {
            html += '<tr><td>';
            html += headers[i];
            html += '</td></tr>';
        }
        document.getElementById('csv_found').innerHTML = html;
        check_for_mustache_elements(); // Update the content so things can be unbolded
    }
    var error_handler = function() {
        alert('Something went wrong while reading');
    }
    var scan_file = function() {
        var html = '';
        if ('files' in fileInput) {
            if (fileInput.files.length == 1) {
                var file = fileInput.files[0];
                // Try to read the file if FileReader supported
                if (window.FileReader) {
                    var reader = new FileReader();
                    reader.readAsText(file);
                    reader.onload = load_handler;
                    reader.onerror = error_handler;
                } else {
                    alert('FileReader are not supported in this browser.');
                }
            }
        }
    }

    fileInput.onchange = scan_file;
}
