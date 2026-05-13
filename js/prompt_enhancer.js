import { app } from "/scripts/app.js";

// Style categories — must match STYLE_CATEGORIES in prompt_enhancer_llm.py
const STYLE_CATEGORIES = {
    "Basic Styles": ["none", "detailed", "photorealistic", "cinematic", "artistic",
                     "minimalist", "vibrant"],
    "Fantasy & Horror": ["fantasy", "horror", "dark fantasy", "heavenly"],
    "Traditional Art": ["oil painting", "watercolor", "abstract expressionist",
                        "hyperrealist", "cubist"],
    "Art Movements": ["art nouveau", "art deco", "baroque", "renaissance", "pop art", "bauhaus",
                      "romanticist", "dada"],
    "Asian Art Styles": ["anime", "studio ghibli", "ukiyo-e", "sumi-e"],
    "Traditional Media": ["oil painting", "watercolor", "pencil sketch",
                          "charcoal drawing", "pastel art"],
    "Digital & Contemporary": ["3d render", "digital art", "concept art", "comic book",
                               "pixel art", "low poly", "isometric"],
    "Genre & Theme": ["cyberpunk", "steampunk", "gothic", "vaporwave", "retro", "vintage"],
    "Decorative Arts": ["stained glass", "mosaic", "street art"],
};

app.registerExtension({
    name: "pinkpixel.prompt_enhancer",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "PromptEnhancer") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                const categoryIndex = this.widgets.findIndex(w => w.name === "style_category");
                const styleIndex = this.widgets.findIndex(w => w.name === "style");

                if (categoryIndex === -1 || styleIndex === -1) return r;

                const categoryWidget = this.widgets[categoryIndex];
                const styleWidget = this.widgets[styleIndex];

                categoryWidget.callback = function(value) {
                    const styles = STYLE_CATEGORIES[value] || ["none"];
                    styleWidget.options.values = styles;
                    styleWidget.value = styles[0];
                    app.graph.setDirtyCanvas(true);
                };

                return r;
            };
        }
    }
});
