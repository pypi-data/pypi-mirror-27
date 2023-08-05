"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
function initDjangoEnv() {
    window.DJANGO = {
        user: { isAuthenticated: true },
        priceRange: { min: 100, max: 30000 },
    };
}
exports.initDjangoEnv = initDjangoEnv;
//# sourceMappingURL=django-env.js.map