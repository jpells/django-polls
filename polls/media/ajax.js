function update_poll() {
    new Ajax.Updater('poll_ajax', '/polls/ajaxrefresh/', {asynchronous:true});
}

function send_form() {
    url = "/polls/"+$('id_slug').value+"/";
    new Ajax.Request(url, {asynchronous:true, parameters:Form.serialize(form)});
    Form.reset(form);
    return false;
}
