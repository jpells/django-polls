function update_poll() {
    new Ajax.Updater('poll_ajax', '/polls/ajaxrefresh/', {asynchronous:true});
}

function send_form() {
    url = "/polls/"+document.getElementById('id_slug').value+"/";
    new Ajax.Request(url, {asynchronous:true, parameters:Form.serialize(form)});
    Form.reset(form);
    update_poll();
    return false;
}
