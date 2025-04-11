'use strict'

const my_red = '#ff808d';
const my_yellow = '#ffdf80';
const my_green = '#80ffc3';
const my_blue = '#80eaff';

const difToColor = new Map();
difToColor.set('practice', my_blue);
difToColor.set('easy', my_green);
difToColor.set('medium', my_yellow);
difToColor.set('nightmare', my_red);

const difToAudio = new Map();
difToAudio.set('practice', mus1);
difToAudio.set('easy', mus2);
difToAudio.set('medium', mus3);
difToAudio.set('nightmare', mus4);

const difToLength = new Map();
difToLength.set('practice', 2*60*1000 + 21*1000 + 270);
difToLength.set('easy', 3*60*1000 + 17*1000 + 512);
difToLength.set('medium', 5*60*1000 + 27*1000 + 344);
difToLength.set('nightmare', 5*60*1000 + 57*1000 + 487);

async function fakeHref(href) {
    await window.fetch(href)
        .then(response => response.text())
        .then((data) => {
            const parser = new DOMParser();
            const newDocument = parser.parseFromString(data, "text/html");
            // const title = newDocument.getElementsByTagName('title')[0].text;
            // window.history.pushState({
            //     'html': data,
            //     'pageTitle': title,
            // }, "", href);
            document.getElementById('mount').innerHTML = newDocument.getElementById('mount').innerHTML;
        });
}


let app = undefined;
let background = undefined;
async function loadCanvas() {
    app = new PIXI.Application();

    await app.init({
        resizeTo: window,
        preference: 'webgl'
    });

    document.body.appendChild(app.canvas);
    background = PIXI.Sprite.from(PIXI.Texture.EMPTY);
    background.width = window.innerWidth;
    background.height = window.innerHeight;
    app.stage.addChild(background);

    const filter = new PIXI.Filter({
        glProgram: new PIXI.GlProgram({
            fragment: index_frag_source,
            vertex: index_vert_source,
        }),
        resources: {
            timeUniforms: {
                uTime: { value: 0.0, type: 'f32' },
            },
        },
    });

    // Add the filter
    app.stage.filters = [filter];

    app.ticker.add((ticker) => {
        filter.resources.timeUniforms.uniforms.uTime += 0.04 * ticker.deltaTime;
    });
}

let gameDifficulty = 'practice';
let gameScore = 0;
let gameScoreThousands = 0;
let fails = 0;
let previousQuestionTime = 0;
let currentQuestionAnswer = "";
function nextQuestion() {
    const questionElem = document.getElementById('question');
    const answersElem = document.getElementById('answers');
    // questionElem.textContent = "";
    // answersElem.textContent = "";

    fetch(`api/v1/question/${gameDifficulty}`)
        .then(response => response.json())
        .then((data) => {
            previousQuestionTime = Date.now();
            fails = 0;
            questionElem.textContent = data['question_text'];
            currentQuestionAnswer = data['choices'][data['correct_idx']];
            if (answersElem.childElementCount !== data['choices'].length) {
                answersElem.textContent = "";
            }
            for (let idx = 0; idx < data['choices'].length; idx++) {
                if (answersElem.childElementCount <= idx) {
                    const elemCol = document.createElement('div');
                    elemCol.setAttribute('class', 'col');
                    const elemButton = document.createElement('button');
                    elemButton.setAttribute('class', "btn btn-lg btn-outline-dark w-100 mt-2");
                    elemButton.textContent = data['choices'][idx];
                    elemButton.onclick = answerButtonPress;
                    elemCol.appendChild(elemButton);
                    answersElem.appendChild(elemCol);
                }
                else {
                    const elemButton = answersElem.children[idx].childNodes[0];
                    elemButton.setAttribute('class', "btn btn-lg btn-outline-dark w-100 mt-2");
                    elemButton.removeAttribute('disabled');
                    elemButton.textContent = data['choices'][idx];
                }
            }
        })
}

function shuffle(array) {
    let currentIndex = array.length;

    // While there remain elements to shuffle...
    while (currentIndex !== 0) {

    // Pick a remaining element...
    let randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }
}

const audioFails = [audioFail1, audioFail2, audioFail3, audioFail4, audioFail5, audioFail6, audioFail7, audioFail8, audioFail9, audioFail10, audioFail11, audioFail12, audioFail13, audioFail14,]
let audioFailIdx = 0;
function answerButtonPress(me) {
    if (me.target.textContent === currentQuestionAnswer) {
        audioSuccess1.play().then();
        const curTime = Date.now();
        const questionScore = 100 - 75 * fails - (curTime - previousQuestionTime)/500;
        gameScore += Math.max(0, questionScore);
        const newThousand = Math.floor(gameScore / 1000);
        if (newThousand > gameScoreThousands) {
            audio1Up.play().then();
            gameScoreThousands = newThousand;
        }
        nextQuestion();
    }
    else {
        if (audioFailIdx === 0) {
            shuffle(audioFails);
        }
        const audioFail = audioFails[audioFailIdx];
        audioFailIdx = (audioFailIdx + 1) % audioFails.length;
        audioFail.play().then();
        fails++;
        me.target.setAttribute('disabled', '');
        me.target.classList.remove('btn-outline-dark');
        me.target.classList.add('btn-danger');
    }
}

function gameEnd() {
    if (gameDifficulty === 'practice') {
        // continue in endless mode
        return;
    }
    const questionElem = document.getElementById('question');
    const answersElem = document.getElementById('answers');
    audioClear.play().then();
    gameScore = Math.floor(gameScore)
    questionElem.textContent = `Score: ${gameScore}`;
    answersElem.textContent = 'Press F5 to try again!';
    // score
}

let gameStartTimeout = 0;
window.onload = (_) => {
    if (typeof PIXI !== 'undefined' && (window.location.pathname === '/' || window.location.pathname === '/leaderboard')) {
        fetchShaders().then(() => {
            loadCanvas().then(_ => console.log("canvased"));
        });
    }

    const enterGameButtonAnim = (mouseEvent) => {
        if (gameStartTimeout !== 0) return;

        audioEnter.play().then();
        const elem = mouseEvent.target;
        gameDifficulty = elem.difficulty;
        elem.focus();   // force highlighted state
        const circle = document.createElement('div');
        circle.classList.add('circle');
        circle.style.left = mouseEvent.x.toString() + 'px';
        circle.style.top = mouseEvent.y.toString() + 'px';
        const btnStyle = window.getComputedStyle(elem);
        circle.style.backgroundColor = btnStyle.borderColor;
        document.getElementById('overlays').appendChild(circle);


        gameStartTimeout = window.setTimeout(() => {
            fakeHref(`api/v1/game/${gameDifficulty}`).then(() => {
                document.getElementsByTagName('canvas')[0].remove();
                document.documentElement.setAttribute('data-bs-theme', 'light');
                document.getElementsByTagName('body')[0].style.backgroundColor = difToColor.get(gameDifficulty);
                document.getElementById('overlays').innerHTML = "";

                const bgm = difToAudio.get(gameDifficulty);
                bgm.play();

                nextQuestion();

                window.setTimeout(gameEnd, difToLength.get(gameDifficulty));
            });

        }, 500);
    }

    let btn;
    btn = document.getElementById('btn-practice');
    if (btn !== null) { btn.onclick = enterGameButtonAnim; btn.difficulty = 'practice'; }
    btn = document.getElementById('btn-easy');
    if (btn !== null) { btn.onclick = enterGameButtonAnim; btn.difficulty = 'easy'; }
    btn = document.getElementById('btn-medium');
    if (btn !== null) { btn.onclick = enterGameButtonAnim; btn.difficulty = 'medium'; }
    btn = document.getElementById('btn-nightmare');
    if (btn !== null) { btn.onclick = enterGameButtonAnim; btn.difficulty = 'nightmare'; }

};

let timeoutId = 0;
window.onresize = (_) => {
    if (app !== undefined) {
        // refreshing timeout
        const refreshStage = () => {
            app.stage.setSize(window.innerWidth, window.innerHeight);
            timeoutId = 0;
        }

        if (timeoutId !== 0) {
            window.clearTimeout(timeoutId);
        }
        timeoutId = window.setTimeout(refreshStage, 100);
    }
};

// debug keys
window.onkeydown = (ke) => {
    if (ke.key === "T") {
        mus1.pause();
        mus2.pause();
        mus3.pause();
        mus4.pause();
        document.querySelectorAll('audio').forEach(el => el.pause());
        gameEnd();
    }
}