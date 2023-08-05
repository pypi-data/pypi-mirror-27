import {Params} from '@angular/router'
import {UrlSegment} from '@angular/router'
import {ActivatedRouteSnapshot} from '@angular/router'
import {routeLocation} from 'app/app.routing'


export function genRouteSnapshot(params: Params = {}): ActivatedRouteSnapshot {
    // TODO use a const from app.routing instead of the 'catalog' str
    let urlSegment = new UrlSegment('catalog', params)
    let snapshot: ActivatedRouteSnapshot = {
        url: [urlSegment],
        params: params,
        data: {location: routeLocation.root},
    } as any
    return snapshot
}
