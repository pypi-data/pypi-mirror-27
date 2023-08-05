import {QueryDataToRouteParamsSerializer} from 'app/shared/query-data/serializers/route-params'
import {QueryDataGenerator} from 'testutils/generators/query-data'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {RouteSnapshotToQueryDataDeserializer} from 'app/shared/query-data/deserializers/route-snapshot'
import {AttrimOption} from 'app/shared/query-data/query-data.model'
import {genRouteSnapshot} from 'testutils/generators/route'


describe('query data to route params serializers', () => {
    it('encodes & decodes queryData to & from route params', () => {
        let gen = new QueryDataGenerator()
        let dataSource: QueryData = gen.data()

        let dataSerializer = new QueryDataToRouteParamsSerializer()
        let dataSerialized = dataSerializer.toRouteParams(dataSource)
        let dataRouteSnapshot = genRouteSnapshot(dataSerialized)
        let dataDeserializer = new RouteSnapshotToQueryDataDeserializer()
        let dataDeserialized: QueryData = dataDeserializer.toQueryData(dataRouteSnapshot)

        expect(dataDeserialized.sorting).toBe(dataSource.sorting)

        for (let cls of dataDeserialized.attrimClsArray) {
            let isClsSource = (clsToCheck) => {
                return cls.code === clsToCheck.code
            }
            let clsSource = dataSource.attrimClsArray.find(isClsSource)
            expect(cls.code).toBe(clsSource!!.code)

            for (let optionDecoded of cls.options) {
                let isSourceOption = (option: AttrimOption) => {
                    return option.value === optionDecoded.value
                }
                let optionSource = clsSource!!.options.find(isSourceOption)
                expect(optionDecoded.value).toBe(optionSource!!.value)
                expect(optionDecoded.isSelected).toBe(optionSource!!.isSelected)
            }
        }

        expect(dataDeserialized.pageCurrent).toBe(dataSource.pageCurrent)
    })
})
