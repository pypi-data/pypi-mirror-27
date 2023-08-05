import {SlimLoadingBarService} from 'ng2-slim-loading-bar'


export function asyncWithLoadingBar(
    target: Object,
    propertyKey: string,
    descriptor: TypedPropertyDescriptor<any>,
): TypedPropertyDescriptor<any> {
    let originalMethod = descriptor.value
    descriptor.value = async function(...args: any[]): Promise<any> {
        (this as Loadable).loadingBarService.start();
        let result: any = await originalMethod.apply(this, args);
        (this as Loadable).loadingBarService.complete();
        return result;
    }
    return descriptor
}


export interface Loadable {
    loadingBarService: SlimLoadingBarService
}
