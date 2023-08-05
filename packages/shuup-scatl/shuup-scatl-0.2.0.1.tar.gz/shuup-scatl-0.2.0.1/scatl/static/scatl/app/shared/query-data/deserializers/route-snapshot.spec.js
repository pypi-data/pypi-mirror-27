"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const route_snapshot_1 = require("app/shared/query-data/deserializers/route-snapshot");
describe('route snapshot deserializer', () => {
    let self = {
        deserializer: new route_snapshot_1.RouteSnapshotToQueryDataDeserializer()
    };
    it('throws an error on a price range with neg negative', () => {
        let routeSnapshotFake = createFakeRouteSnapshot({ priceRange: '-453~5434' });
        expect(() => { self.deserializer.toQueryData(routeSnapshotFake); })
            .toThrowError('Invalid price range parameter');
    });
    it('throws an error on a price range without a splitter', () => {
        let routeSnapshotFake = createFakeRouteSnapshot({ priceRange: '4535434' });
        expect(() => { self.deserializer.toQueryData(routeSnapshotFake); })
            .toThrowError('Invalid price range parameter');
    });
    it('throws an error on a price range that contains non-number chars', () => {
        let routeSnapshotFake = createFakeRouteSnapshot({ priceRange: 'z453~5434' });
        expect(() => { self.deserializer.toQueryData(routeSnapshotFake); })
            .toThrowError('Invalid price range parameter');
    });
    function createFakeRouteSnapshot(args) {
        let routeSnapshotFake = {
            data: {
                location: '',
            },
            params: {
                'filter.price': args.priceRange
            },
        };
        return routeSnapshotFake;
    }
});
//# sourceMappingURL=route-snapshot.spec.js.map