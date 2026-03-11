import { Component } from '@angular/core';
import { NzTableModule } from 'ng-zorro-antd/table';
import { NzDividerModule } from 'ng-zorro-antd/divider';
import { FormsModule } from '@angular/forms';
import { __ENTITY_PASCAL__ } from './__ENTITY_KEBAB__';
import { __ENTITY_PASCAL__Service } from './__ENTITY_KEBAB__.service';
import { Alert } from '../alert/alert.component';

@Component({
    selector: 'app-__ENTITY_KEBAB__',
    imports: [NzTableModule, NzDividerModule, FormsModule, Alert],
    templateUrl: './__ENTITY_KEBAB__.component.html',
    styleUrl: './__ENTITY_KEBAB__.component.css'
})

export class __ENTITY_PASCAL__Component {
    __ENTITY_CAMEL__Collection: __ENTITY_PASCAL__[] = [];
    __ENTITY_CAMEL__CacheCollection: __ENTITY_PASCAL__[] = [];
    newItem: __ENTITY_PASCAL__ = {} as any;
    nzScroll = { x: '800px', y: '600px' }; // TODO: implement dynamic sizing

    constructor(private __ENTITY_CAMEL__Service: __ENTITY_PASCAL__Service, private alert: Alert) { }

    ngOnInit(): void {
        this.read();
    }

    isNullOrEmpty(o: __ENTITY_PASCAL__) {
        if (Object.getOwnPropertyNames(o).length === 0 && o.constructor === Object)
            return true; // null

        if (Object.keys(o).map(e => (o as any)[e]).every(a => a.length === 0)) {
            return true; // empty
        }
        return false;
    };

    saveCollection(): void {
        this.__ENTITY_CAMEL__CacheCollection = [...this.__ENTITY_CAMEL__Collection].map((x) => ({ ...x }));
    }

    restoreCollection(): void {
        this.__ENTITY_CAMEL__Collection = [...this.__ENTITY_CAMEL__CacheCollection].map((x) => ({ ...x }));
    }

    create(): void {
        this.__ENTITY_CAMEL__Service.create(this.newItem)
            .subscribe(response => {
                if (response.status === 'success') {
                    this.__ENTITY_CAMEL__Collection.push(response.result[0]);
                    this.saveCollection();
                    this.alert.success("added data");
                } else {
                    // restore not required as no record created
                    this.alert.error(`could not add data: ${response.status}`);
                }
                this.newItem = {} as any;
            });
    }

    read(): void {
        this.__ENTITY_CAMEL__Service.read()
            .subscribe(response => {
                if (response.status === 'success') {
                    this.__ENTITY_CAMEL__Collection = response.result
                    this.saveCollection();
                    this.alert.success("read data");
                } else {
                    this.restoreCollection();
                    this.alert.error(`could not read data: ${response.status}`);
                }
            });
    }

    update(item: __ENTITY_PASCAL__) {
        this.__ENTITY_CAMEL__Service.update(item)
            .subscribe(response => {
                if (response.status === 'success') {
                    this.saveCollection();
                    this.alert.success("saved data");
                } else {
                    this.restoreCollection();
                    this.alert.error(`could not save data: ${response.status}`);
                }
            });
    }

    delete(item: __ENTITY_PASCAL__) {
        this.__ENTITY_CAMEL__Service.delete(item.__ENTITY_ID__).subscribe(response => {
            if (response.status === 'success') {
                this.__ENTITY_CAMEL__Collection = this.__ENTITY_CAMEL__Collection.filter(i => i !== item);
                this.saveCollection();
                this.alert.success("deleted data");
            } else {
                // restore not required as no record deleted
                this.alert.error(`could not delete data: ${response.status}`);
            }
        });
    }

}
