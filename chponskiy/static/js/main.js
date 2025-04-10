'use strict'

const my_red = '#ff808d';
const my_yellow = '#ff808d';
const my_green = '#ffdf80';
const my_blue = '#80eaff';

const difToColor = new Map();
difToColor.set('practice', my_blue);
difToColor.set('easy', my_green);
difToColor.set('medium', my_yellow);
difToColor.set('nightmare', my_red);

const difToAudio = new Map();
difToAudio.set('practice', mus1);

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

function gameBegin() {
    console.log("Gaming!");
}

let gameStartTimeout = 0;
window.onload = (_) => {
    if (typeof PIXI !== 'undefined' && window.location.pathname === '/') {
        fetchShaders().then(() => {
            loadCanvas().then(_ => console.log("canvased"));
        });
    }

    const enterGameButtonAnim = (mouseEvent) => {
        if (gameStartTimeout !== 0) return;

        audioEnter.play();
        const elem = mouseEvent.target;
        elem.focus();   // force highlighted state
        const circle = document.createElement('div');
        circle.classList.add('circle');
        circle.style.left = mouseEvent.x.toString() + 'px';
        circle.style.top = mouseEvent.y.toString() + 'px';
        const btnStyle = window.getComputedStyle(elem);
        circle.style.backgroundColor = btnStyle.borderColor;
        document.getElementById('overlays').appendChild(circle);


        gameStartTimeout = window.setTimeout(() => {
            fakeHref(`api/v1/game/${elem.difficulty}`).then(() => {
                document.getElementsByTagName('canvas')[0].remove();
                document.documentElement.setAttribute('data-bs-theme', 'light');
                document.getElementsByTagName('body')[0].style.backgroundColor = difToColor.get(elem.difficulty);
                document.getElementById('overlays').innerHTML = "";

                const bgm = difToAudio.get(elem.difficulty);
                bgm.play();
            });

        }, 2000);
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
