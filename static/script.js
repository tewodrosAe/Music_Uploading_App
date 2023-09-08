"use strict";
const guard = [
    {
        name: "Tedy",
        age: "21",
        school: "AAU"
    },
    {
        name: "Nahom",
        age: "21",
        school: "st Mary"
    }
]

const guards = new Object
console.log(guard[0]["name"])

let btn = document.querySelector("#register");
let btn2 = document.querySelector("#login");
let cardFront = document.querySelector(".cardfrontsa");
let cardBack = document.querySelector(".cardbacksa");
const body = document.querySelector('body');
const section = document.querySelectorAll('.containera');
if(cardFront){
btn.addEventListener("click",function(){
    cardFront.style.transform = "rotateY(180deg)";
    cardBack.style.transform = "none";
    });
    
btn2.addEventListener("click",function(){
    cardFront.style.transform = "none";
    cardBack.style.transform = "rotateY(180deg)";
})
}


const name = document.querySelector('.name');
const password = document.querySelector('.password');
const confirm = document.querySelector('.confirm');
const email = document.querySelector('.email');
const submit = document.querySelector('.submit');
const form = document.querySelector('.form');
const forms = document.querySelector('.formsa');
const errorElement = document.querySelector(".error")
const errorElements = document.querySelector(".errors")

if(form){
form.addEventListener('submit',(e)=>{
    let error = [];
    if (password.value.length < 6){
        error.push("Password must be more than 6 characters")
    }
    if (password.value.length === '' || password.value.length == null){
        error.push("Password required")
    }
    if (error.length > 0){
        e.preventDefault();
        errorElement.innerText = error.join(', ')
    }
})
}
const progress = document.getElementById('progressbar');
const totalHeight = document.body.scrollHeight - window.innerHeight;
window.onscroll = function(){
    const progressHeight = (window.pageYOffset / totalHeight) * 100;
    progress.style.width = progressHeight + '%';
}
const visibleButton = document.getElementById("poo");
const invisibleButton = document.getElementById("file");
const para = document.getElementById("nana")
const continueBtn = document.getElementById("poos");
const fileName = document.getElementById("fila");
const icon = document.getElementById("inoi")
const upload = document.getElementById("soop")
const validForm = document.querySelector(".valid")
if(icon){
visibleButton.addEventListener('click',function(){
  
    invisibleButton.click();
})
invisibleButton.addEventListener("change",function(){
    if (invisibleButton.value){
        visibleButton.style.visibility = "hidden";
        para.style.visibility = "hidden";
        continueBtn.style.visibility = "visible";
        fileName.innerHTML += invisibleButton.value.match( /[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
        fileName.style.visibility = "visible";
    }
})
continueBtn.addEventListener("click",function(){
    upload.style.visibility = "visible";
    continueBtn.style.visibility = "hidden";
    validForm.style.visibility = "visible";
    fileName.style.visibility = "hidden"; 
})
}
const all = document.getElementById("together")
const play = document.querySelectorAll(".fa-play-circle")
const video = document.getElementById("video")
const pause = document.querySelectorAll(".fa-pause-circle")
const audio = document.querySelectorAll(".audio")
const volumeSlider = document.querySelectorAll("#volume_slider")
const volumeButton = document.querySelectorAll(".fa-volume-up")
const start = document.querySelectorAll(".start")
const end = document.querySelectorAll(".end")
const userNames = document.querySelectorAll(".user_names") 
for(let i = 0; i < play.length ;i++){
    play[i].addEventListener("click",function(){
        for(let j = 0; j < play.length; j++){
            play[j].style.visibility = "visible";
            audio[j].pause();
            pause[j].style.visibility = "hidden";
            userNames[j].style.position = "absolute";
            userNames[j].style.visibility = "hidden";
            video.currentTime = 0;
        }
        userNames[i].style.position = "static";
        userNames[i].style.visibility = "visible";
        audio[i].play()  
        play[i].style.visibility = "hidden";
        pause[i].style.visibility = "visible";
        video.play();
        video.style.filter = "blur(0.5px)";
        all.style.animationPlayState = 'running';
    })
}
for (let i = 0; i < pause.length; i++){
    pause[i].addEventListener("click",function(){
        audio[i].pause()
        play[i].style.visibility = "visible";
        pause[i].style.visibility = "hidden";
        userNames[i].style.position = "absolute";
        userNames[i].style.visibility = "hidden";
        video.pause()
        video.style.filter = "blur(4px)";
        all.style.animationPlayState = 'paused';
    })
}

const slider = document.querySelectorAll("#slider");
for (let i = 0; i < slider.length; i++){
    slider[i].addEventListener("change",() => {
        let sliderPosition = audio[i].duration * (slider[i].value / 100)
        audio[i].currentTime = sliderPosition;
    })
    audio[i].addEventListener('timeupdate',() => {
        let position = audio[i].currentTime * (100 / audio[i].duration)
        slider[i].value = position;
        if(audio[i].currentTime == audio[i].duration){
            pause[i].click();
        }
})
    audio[i].addEventListener('timeupdate',() => {
        let current_minute = Math.floor(audio[i].currentTime / 60)
        let current_second =  Math.floor(audio[i].currentTime - (current_minute * 60))
        if ( current_second < 10){
            current_second = "0" + current_second;
        }
        start[i].innerHTML = current_minute + ":" + current_second;
})

}
const volume_on = document.querySelectorAll(".fa-volume-up")
const volume_off = document.querySelectorAll(".fa-volume-off")
for(let i = 0; i < volumeButton.length;i++){
    volumeSlider[i].addEventListener('change',() => {
    audio[i].volume = volumeSlider[i].value / 100;
})
    volume_on[i].onclick = () =>{
        volume_on[i].style.visibility = "hidden";
        volume_off[i].style.visibility = "visible";
        audio[i].muted = true;
    }
    volume_off[i].onclick = () => {
        volume_on[i].style.visibility = "visible";
        volume_off[i].style.visibility = "hidden";
        audio[i].muted = false;
    }
}
window.onpageshow = () => {
            setTimeout(() => 
            {for(let i = 0; i < volumeButton.length;i++){
            let duration_minute = Math.floor(audio[i].duration / 60);
            let duration_second = Math.floor(audio[i].duration - (duration_minute * 60));
            end[i].innerText = duration_minute + ":" + duration_second;
            audio[i].volume = 0.5;
        }    },300)
         
}
const times = document.getElementById("x")
const whole = document.getElementById("donate")
const inner =  document.getElementById("insout")
const donateBtn = document.getElementById("donate_btn")
times.onclick = () =>{
    whole.style.zIndex = "-1";
    inner.style.zIndex = "-1";
}
whole.onclick = () =>{
    whole.style.zIndex = "-1";
    inner.style.zIndex = "-1";
}
donateBtn.onclick = () => {
    whole.style.zIndex = "100";
    inner.style.zIndex = "101";
}
const pic = document.getElementById("pp")
const profile = document.getElementById("profile")
const togethers = document.querySelector(".togethers")
const insouts = document.querySelector(".insouts")
const ask = document.getElementById("inne")
if(pic){
pic.onclick = () =>{
    profile.click()
}
profile.onchange = () =>{
    togethers.style.zIndex = "99";
    insouts.style.zIndex = "100";
    ask.innerHTML = "Are you sure you want to make " + profile.value.match( /[\/\\]([\w\d\s\.\-\(\)]+)$/)[1] + " your new profile picture?"
}
}

const usr = document.querySelectorAll(".user_names")
const btnName = document.querySelectorAll(".btn_name")
const userInput = document.querySelectorAll(".user_input")
for(let i = 0; i < userInput.length; i++){
    usr[i].onclick = () => {
        userInput[i].value = btnName[i].innerHTML
        btnName[i].click()
    }
}

document.querySelector("#no").onclick = () =>{
    togethers.style.zIndex = "-1";
    insouts.style.zIndex = "-1";
    profile.value = null;
}
