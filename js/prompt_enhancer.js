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
        if (nodeData.name !== "PromptEnhancer") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function() {
            const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

            const categoryWidget = this.widgets.find(w => w.name === "style_category");
            const styleWidget = this.widgets.find(w => w.name === "style");

            if (!categoryWidget || !styleWidget) return r;

            // Track last known category to detect changes
            this._peLastCategory = categoryWidget.value;

            // Wrap the existing combo callback — ComfyUI combo widgets
            // fire the `callback` on selection change
            const origCallback = categoryWidget.callback;
            categoryWidget.callback = function(value) {
                if (origCallback) origCallback.call(this, value);
                updateStyles(this);
            };

            // Also hook the original callback in case ComfyUI uses a different mechanism
            const self = this;
            Object.defineProperty(this, "__peUpdateStyles", {
                get() {
                    return function() {
                        const cat = categoryWidget.value;
                        if (cat !== self._peLastCategory) {
                            self._peLastCategory = cat;
                            const styles = STYLE_CATEGORIES[cat] || ["none"];
                            styleWidget.options.values = styles;
                            // Reset to first valid style if current value is not in the new list
                            if (!styles.includes(styleWidget.value)) {
                                styleWidget.value = styles[0];
                            }
                        }
                    };
                },
                set() {},
                enumerable: false,
            });

            return r;
        };

        // onDrawForeground runs every frame — check for category change here
        const onDrawForeground = nodeType.prototype.onDrawForeground;
        nodeType.prototype.onDrawForeground = function() {
            const r = onDrawForeground ? onDrawForeground.apply(this, arguments) : undefined;

            const categoryWidget = this.widgets.find(w => w.name === "style_category");
            const styleWidget = this.widgets.find(w => w.name === "style");

            if (!categoryWidget || !styleWidget) return r;

            const cat = categoryWidget.value;
            if (cat !== this._peLastCategory) {
                this._peLastCategory = cat;
                const styles = STYLE_CATEGORIES[cat] || ["none"];
                styleWidget.options.values = styles;
                if (!styles.includes(styleWidget.value)) {
                    styleWidget.value = styles[0];
                }
            }

            return r;
        };
    }
});
