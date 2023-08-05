"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const router_1 = require("@angular/router");
const catalog_comp_1 = require("app/catalog.comp");
exports.routeLocation = {
    root: 'root',
    category: 'category',
};
const routes = [
    {
        // TODO allow to defined it with the plugin or admin config
        path: 'catalog',
        component: catalog_comp_1.CatalogComponent,
        data: {
            location: exports.routeLocation.root,
        },
    },
    // TODO: don't forget about 404 here
    {
        path: '**',
        component: catalog_comp_1.CatalogComponent,
        data: {
            location: exports.routeLocation.category,
        },
    },
];
exports.routing = router_1.RouterModule.forRoot(routes);
//# sourceMappingURL=app.routing.js.map