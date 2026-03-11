import { Component, ViewChild } from '@angular/core';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDialog } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatPaginator, MatPaginatorModule, PageEvent } from '@angular/material/paginator';

import { __ENTITY_PASCAL__FormComponent } from './__ENTITY_KEBAB__-form.component'
import { __ENTITY_PASCAL__ApiService } from './__ENTITY_KEBAB__-api.service';
import { __ENTITY_PASCAL__View } from './__ENTITY_KEBAB__.view';
import { __ENTITY_PASCAL__ViewModel } from './__ENTITY_KEBAB__.viewmodel';

import { Alert } from "../../components/alert.component/alert.component";

@Component({
    selector: 'app-__ENTITY_KEBAB__',
    imports: [
        MatTableModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        MatIconModule,
        MatPaginatorModule,
        Alert,
    ],
    templateUrl: './__ENTITY_KEBAB__.component.html',
    styleUrl: './__ENTITY_KEBAB__.component.css'
})
export class __ENTITY_PASCAL__Component {
    columnNames: string[] = [__KEYS_PASCAL_SPACED__QUOTED__];
    displayedColumns: string[] = [__KEYS_INDEXES_QUOTED__];
    dataSource = new MatTableDataSource<__ENTITY_PASCAL__View>([]);

    constructor(
        private alert: Alert,
        private dialog: MatDialog,
        private service: __ENTITY_PASCAL__ApiService,
    ) { }

    configureDisplayedColumns() {
        let columnNames: string[] = [];
        let displayedColumns: string[] = [];

        this.service.apiModel.entity_fields.forEach((v, i) => {
            columnNames.push(v);
            if (!v.startsWith('--hide')) {
                displayedColumns.push(`${i}`);
            }
        });

        if (columnNames.length && displayedColumns.length) {
            this.columnNames = columnNames;
            this.displayedColumns = displayedColumns;
        }
    }

    ngOnInit(): void {
        this.service.readApiModel()
            .subscribe(response =>
                this.handleResponse(response, () => {
                    this.configureDisplayedColumns();
                    this.onDataChange();
                })
            );
    }

    onDataChange(): void {
        this.dataSource = new MatTableDataSource(this.service.apiModel.views);
        this.paginatorPageSize = this.service.apiModel._paging.page_size;
        this.paginator.length = this.service.apiModel._paging.entity_count;
    }

    handleResponse(response: any, action: any) {
        if (response.status === 'success') {
            action();
            this.alert.success("read data");
        } else {
            this.alert.error(`could not read data: ${response.status}`);
        }
    }

    applyFilter(event: Event) {
        const filterValue = (event.target as HTMLInputElement).value;
        this.dataSource.filter = filterValue.trim().toLowerCase();
    }

    onClickAdd() {
        let createItem = {
            entity: __ENTITY_PASCAL__ViewModel.createView(),
            constraints: this.service.apiModel.references
        };

        const dialogRef = this.dialog.open(__ENTITY_PASCAL__FormComponent, {
            maxWidth: '100vw',
            maxHeight: '100vh',
            height: '80%',
            width: '40%',
            data: {
                item: createItem,
                columnNames: this.columnNames,
                crudMode: "Create",
                crudAction: "Save",
                hideDelete: true
            }
        });

        dialogRef.afterClosed().subscribe(result => {
            // clicking outside of the dialog returns undefined
            if (result === undefined || result === 'cancel') {
                return;
            }

            if (result == 'action') {
                this.service.createEntity(createItem.entity)
                    .subscribe(response => {
                        if (response.status === 'success') {
                            this.alert.success("added data");
                            this.onDataChange();
                        } else {
                            this.alert.error(`could not add data: ${response.status}`);
                        }
                    });
            }
        });
    }

    onClickEdit(item: __ENTITY_PASCAL__View) {
        let updateItem = {
            entity: Object.assign({}, item),
            constraints: this.service.apiModel.references
        };

        const dialogRef = this.dialog.open(__ENTITY_PASCAL__FormComponent, {
            maxWidth: '100vw',
            maxHeight: '100vh',
            height: '80%',
            width: '40%',
            data: {
                item: updateItem,
                columnNames: this.columnNames,
                crudMode: "Edit",
                crudAction: "Save"
            }
        });
        dialogRef.afterClosed().subscribe(result => {

            // clicking outside of the dialog returns undefined
            if (result === undefined || result === 'cancel') {
                // no edits to revert as item is a copy
                return;
            }

            if (result === 'delete') {
                this.service.deleteEntity(item)
                    .subscribe(response => {
                        if (response.status === 'success') {
                            this.alert.success("deleted data");
                            this.onDataChange();
                        } else {
                            this.alert.error(`could not delete data: ${response.status}`);
                        }
                    });
            }

            if (result == 'action') {
                this.service.updateEntity(updateItem.entity)
                    .subscribe(response => {
                        if (response.status === 'success') {
                            this.alert.success("saved data");
                            this.onDataChange();
                        } else {
                            this.alert.error(`could not save data: ${response.status}`);
                        }
                    });
            }
        });
    }

    // ---------------------------------------------------------------------------------------------------------------------------------------
    // NAVIGATION/PAGING

    @ViewChild(MatPaginator)
    paginator: MatPaginator = new MatPaginator;

    paginatorPageSize = 0;
    paginatorPageSizeOptions = [5, 10, 25];
    paginatorHidePageSize = false;
    paginatorShowPageSizeOptions = true;
    paginatorShowFirstLastButtons = true;
    paginatorDisabled = false;

    handlePaginatorEvent(e: PageEvent) {

        if (e.pageSize != this.paginatorPageSize) {
            this.service.changePageSize(e.pageSize).subscribe((response: { status: string; }) => {
                if (response.status === 'success') {
                    this.alert.success("read data");
                    this.onDataChange();
                    this.paginator.pageIndex = 0;

                } else {
                    this.alert.warn(`invalid page size action: ${response.status}`);
                }
            })
            return; // suppress weird double-event
        }

        let diff = e.previousPageIndex ? e.pageIndex - e.previousPageIndex : e.pageIndex;
        let func;
        if (this.service.apiModel._links.last && diff > 1) func = this.service.lastPage();
        else if (this.service.apiModel._links.next && diff > 0) func = this.service.nextPage();
        else if (this.service.apiModel._links.first && diff < -1) func = this.service.firstPage();
        else if (this.service.apiModel._links.prev && diff < 0) func = this.service.previousPage();
        else return;

        func.subscribe((response: { status: string; }) => {
            if (response.status === 'success') {
                this.alert.success("read data");
                this.onDataChange();
            } else {
                this.alert.warn(`invalid navigation action: ${response.status}`);
            }
        })
    }

}
