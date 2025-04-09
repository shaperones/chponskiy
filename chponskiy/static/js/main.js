'use strict'

function fakeHref(href) {
    window.fetch(href)
        .then(response => response.text())
        .then((data) => {
            const parser = new DOMParser();
            const newDocument = parser.parseFromString(data, "text/html");
            const title = newDocument.getElementsByTagName('title')[0].text;
            window.history.pushState({
                'html': data,
                'pageTitle': title,
            }, "", href);
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

window.onload = (_) => {
    if (typeof PIXI !== 'undefined') {
        fetchShaders().then(() => {
            loadCanvas().then(_ => console.log("canvased"));
        });
    }

    const fakifyById = (elemId) => {
        let elem = document.getElementById(elemId);
        if (elem !== null) {
            elem.addEventListener('click', (e) => {
                e.preventDefault();
                fakeHref(elem.href);
            });
        }
    }

    // turned out that this looks not as good
    // fakifyById('a-login');
    // fakifyById('a-register');
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
