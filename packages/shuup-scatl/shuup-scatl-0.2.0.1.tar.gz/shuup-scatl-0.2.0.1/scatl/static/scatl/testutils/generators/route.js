"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const router_1 = require("@angular/router");
const app_routing_1 = require("app/app.routing");
function genRouteSnapshot(params = {}) {
    // TODO use a const from app.routing instead of the 'catalog' str
    let urlSegment = new router_1.UrlSegment('catalog', params);
    let snapshot = {
        url: [urlSegment],
        params: params,
        data: { location: app_routing_1.routeLocation.root },
    };
    return snapshot;
}
exports.genRouteSnapshot = genRouteSnapshot;
//# sourceMappingURL=route.js.map