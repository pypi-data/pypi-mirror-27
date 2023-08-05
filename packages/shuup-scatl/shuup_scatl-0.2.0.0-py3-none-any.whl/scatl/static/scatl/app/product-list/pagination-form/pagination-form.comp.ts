import {Component} from '@angular/core'
import {Input} from '@angular/core'
import {Output} from '@angular/core'
import {EventEmitter} from '@angular/core'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {PageNum} from 'app/shared/query-data/query-data.model'
import {ViewEncapsulation} from '@angular/core'


@Component({
    selector: 'pagination-form',
    moduleId: module.id,
    templateUrl: 'pagination-form.comp.html',
    styleUrls: ['pagination-form.comp.css'],
    encapsulation: ViewEncapsulation.None,
})
export class PaginationFormComponent {
    @Input()
    queryData: QueryData

    @Output()
    updatedEvent: EventEmitter<void> = new EventEmitter<void>()

    updateQueryData() {
        this.updatedEvent.emit()
    }

    protected setPage(pageRaw: string | PageNum) {
        this.queryData.pageCurrent = Number(pageRaw)
        this.updatedEvent.emit()
    }

    protected isCurrentPage(pageRaw: string | PageNum): boolean {
        let page = Number(pageRaw)
        return this.queryData.pageCurrent === page
    }

    protected isEndButtonShouldBePresent(): boolean {
        return this.queryData.pageFirst !== this.queryData.pageLast
    }
}
