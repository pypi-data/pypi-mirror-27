"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const route_params_1 = require("app/shared/query-data/serializers/route-params");
const query_data_1 = require("testutils/generators/query-data");
const route_snapshot_1 = require("app/shared/query-data/deserializers/route-snapshot");
const route_1 = require("testutils/generators/route");
describe('query data to route params serializers', () => {
    it('encodes & decodes queryData to & from route params', () => {
        let gen = new query_data_1.QueryDataGenerator();
        let dataSource = gen.data();
        let dataSerializer = new route_params_1.QueryDataToRouteParamsSerializer();
        let dataSerialized = dataSerializer.toRouteParams(dataSource);
        let dataRouteSnapshot = route_1.genRouteSnapshot(dataSerialized);
        let dataDeserializer = new route_snapshot_1.RouteSnapshotToQueryDataDeserializer();
        let dataDeserialized = dataDeserializer.toQueryData(dataRouteSnapshot);
        expect(dataDeserialized.sorting).toBe(dataSource.sorting);
        for (let cls of dataDeserialized.attrimClsArray) {
            let isClsSource = (clsToCheck) => {
                return cls.code === clsToCheck.code;
            };
            let clsSource = dataSource.attrimClsArray.find(isClsSource);
            expect(cls.code).toBe(clsSource.code);
            for (let optionDecoded of cls.options) {
                let isSourceOption = (option) => {
                    return option.value === optionDecoded.value;
                };
                let optionSource = clsSource.options.find(isSourceOption);
                expect(optionDecoded.value).toBe(optionSource.value);
                expect(optionDecoded.isSelected).toBe(optionSource.isSelected);
            }
        }
        expect(dataDeserialized.pageCurrent).toBe(dataSource.pageCurrent);
    });
});
//# sourceMappingURL=route-params.spec.js.map