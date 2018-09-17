function MsgJStoTd(string) {
    return string.replace(/\n\n/g, '<br>');
}

function MsgTDtoTextarea(string) {
    return string.replace(/<br>/g, '\n');
}

function MsgTextareaToJS(string) {
    return string.replace(/\n/g, '\n\n');
}

function MsgTextareaToTD(string) {
    return string.replace(/\n/g, '<br>');
}

function InitTextarea(ta) {
    ta.setAttribute('style', 'height:' + (ta.scrollHeight) + 'px;overflow-y:hidden;');
    ta.addEventListener("input", OnInput, false);
}

function OnPageRender() {
    var rows = document.getElementsByTagName('tr');
    for (var i = 1; i < rows.length; i++) {
        if (rows[i].hasAttribute("segment")) {
            OnRowRender(rows[i]);
        }
    }
}

function OnRowRender(row) {
    var cells = row.getElementsByTagName("td");
    var source = cells[1].innerHTML;
    var transl = cells[2].innerHTML;
    <!--cell is in white list, needs no translation-->
    if (row.hasAttribute("whitelist")) {
        row.className = "whitelist";
    }
    <!--cess is New-->
    else if (source == transl) {
        row.className = "new_segment";
    }
    <!--cell is Translated-->
    else {
        row.className = "old_segment";
    }
}

function OnInput() {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
}

function OnCellClick(cell) {

    if (activeCell == cell) {
        return;
    }
    else if (activeCell != null) {
        ResetCell(activeCell);
    }
    var content = cell.innerHTML;
    while (cell.firstChild)
        cell.removeChild(cell.firstChild);

    var ta = document.createElement('textarea');
    ta.className = "edited_text";
    <!--var p = e.parentNode;-->
    <!--cell.style.display = "none";-->

    ta.value = MsgTDtoTextarea(content);
    ta.cols = 60;

    cell.appendChild(ta);
    InitTextarea(ta);

    ta.focus();

    activeCell = cell;
}

function ResetCell(cell) {
    var ta = cell.getElementsByTagName("textarea")[0];

    var lang = cell.getAttribute("lang");
    var k = cell.parentElement.getElementsByTagName("td")[0].innerText;
    var t = ta.value;

    cell.removeChild(ta);

    ReportChange(lang, k, MsgTextareaToJS(t));
    cell.innerHTML = MsgTextareaToTD(t);

    OnRowRender(cell.parentNode);
}

function ReportChange(lang, k, v) {
    var request = new XMLHttpRequest();
    request.onload = function() {
        console.log("Request for " + k + ":" + v + "");
        console.log("Status: " + request.status);
        console.log("Response:" + request.responseText);
    }
    request.onreadystatechange = function() {
        if (request.readyState == XMLHttpRequest.DONE) {
            if (request.status != 200) {
                alert(request.statusText);
            }
        }
    }
    request.open("POST", "http://127.0.0.1:5000/report", true);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    var body = JSON.stringify({ "lang": lang, "key": k, "translation": v })
    request.send(body)
}

function onEscapeKeyListener(e) {
    var keyCode = e.which;
    if ((keyCode == 27) && activeCell) {
        ResetCell(activeCell);
        activeCell = null;
    }
}
