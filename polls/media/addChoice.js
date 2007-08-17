function createChoice() {
    choice_count = document.getElementById('id_choice_count');
    choice_count.value = parseInt(choice_count.value) + 1;
    poll_form = document.getElementById('poll_form');
    newitem = '<li><label for="id_choice'+choice_count.value+'-choice">Choice:</label> <input id="id_choice'+choice_count.value+'-choice" type="text" name="choice'+choice_count.value+'-choice" maxlength="200" /><input type="hidden" name="choice'+choice_count.value+'-poll" id="id_choice'+choice_count.value+'-poll" /></li>';
    newnode=document.createElement("span");
    newnode.innerHTML=newitem;
    button=document.getElementById("addChoice");
    poll_form.insertBefore(newnode,button);
}
