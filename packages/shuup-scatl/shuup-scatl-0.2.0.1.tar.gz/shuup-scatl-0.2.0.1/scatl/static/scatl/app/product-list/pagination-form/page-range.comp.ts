import {Component} from '@angular/core'
import {Input} from '@angular/core'
import {Output} from '@angular/core'
import {EventEmitter} from '@angular/core'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {PageNum} from 'app/shared/query-data/query-data.model'
import {PageRangeService} from 'app/product-list/pagination-form/page-range.service'


@Component({
    selector: 'page-range',
    moduleId: module.id,
    templateUrl: 'page-range.comp.html',
})
export class PageRangeComponent {
    @Input()
    queryData: QueryData
    
    @Output()
    updatedEvent: EventEmitter<void> = new EventEmitter<void>()

    protected buttonRange: number = 3

    constructor(
        private pageRangeService: PageRangeService,
    ) { }

    protected setPage(pageRaw: string | number) {
        this.queryData.pageCurrent = Number(pageRaw)
        this.updatedEvent.emit()
    }

    protected getPageArrayRange(): Array<PageNum> {
        return this.pageRangeService.getPageArrayRange({
            pageStart: this.queryData.pageFirst,
            pageEnd: this.queryData.pageLast,
            pageCurrent: this.queryData.pageCurrent,
            range: this.buttonRange,
        })
    }

    protected isCurrentPage(pageRaw: string | number): boolean {
        let page = Number(pageRaw)
        return this.queryData.pageCurrent === page
    }

    protected isLeftEllipsisRequired(): boolean {
        return this.pageRangeService.isLeftEllipsisRequired({
            pageStart: this.queryData.pageFirst,
            pageCurrent: this.queryData.pageCurrent,
            range: this.buttonRange,
        })
    }

    protected isRightEllipsisRequired(): boolean {
        return this.pageRangeService.isRightEllipsisRequired({
            pageEnd: this.queryData.pageLast,
            pageCurrent: this.queryData.pageCurrent,
            range: this.buttonRange,
        })
    }
}
