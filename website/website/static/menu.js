const play = document.getElementById('play')
const socials = document.getElementById('socials')
const hidden_con = document.getElementById('hidden_container')
const social_con = document.getElementById('socials_container')
const help = document.getElementById('help')
const help_con = document.getElementById('help_container')

play.addEventListener('mouseover', function handleMouseOverEvent() {
    hidden_con.style.display = 'block';
});

play.addEventListener('mouseout', function handleMouseOutEvent() {
    hidden_con.style.display = 'none';
});

socials.addEventListener('mouseover', function handleMouseOverEvent() {
    social_con.style.display = 'block';
});

socials.addEventListener('mouseout', function handleMouseOutEvent() {
    social_con.style.display = 'none';
});

hidden_con.addEventListener('mouseover', function handleMouseOverEvent() {
    hidden_con.style.display = 'block';
});

hidden_con.addEventListener('mouseout', function handleMouseOutEvent() {
    hidden_con.style.display = 'none';
});

social_con.addEventListener('mouseover', function handleMouseOverEvent() {
    social_con.style.display = 'block';
});

social_con.addEventListener('mouseout', function handleMouseOutEvent() {
    social_con.style.display = 'none';
});

help.addEventListener('mouseover', function handleMouseOutEvent() {
    help_con.style.display = 'block';
});

help.addEventListener('mouseout', function handleMouseOutEvent() {
    help_con.style.display = 'none';
});

help_con.addEventListener('mouseover', function handleMouseOutEvent() {
    help_con.style.display = 'block';
});

help_con.addEventListener('mouseout', function handleMouseOutEvent() {
    help_con.style.display = 'none';
});

function openBugForm(){
    document.getElementById('bug_form').style.display = "block";
    document.getElementById('feedback_form').style.display = "none";
}

function openFeedbackForm(){
    document.getElementById('feedback_form').style.display = "block";
    document.getElementById('bug_form').style.display = "none";
}

function closeBugForm(){
    document.getElementById('bug_form').style.display = "none";
}

function closeFeedbackForm(){
    document.getElementById('feedback_form').style.display = "none";
}

function openChat() {
    document.getElementById("myForm").style.display = "block";
    document.getElementById("chat_button").style.display = "none";
    }

function closeChat() {
document.getElementById("myForm").style.display = "none";
document.getElementById("chat_button").style.display = "block";
}

function openChatBox(){
    if (document.getElementById('chatbox_content').style.display == "none"){
        document.getElementById('chatbox_content').style.display = "block";
    }
    else {
        document.getElementById('chatbox_content').style.display = "none";
    }
}