import {Component} from '@angular/core'
import {Input} from '@angular/core'
import {Output} from '@angular/core'
import {EventEmitter} from '@angular/core'

import {QueryData} from 'app/shared/query-data/query-data.model'


@Component({
    selector: 'shuup-form',
    moduleId: module.id,
    templateUrl: 'shuup-form.comp.html',
})
export class AttrimFormComponent {
    @Input()
    queryData: QueryData

    @Output()
    updated: EventEmitter<void> = new EventEmitter<void>()
}
