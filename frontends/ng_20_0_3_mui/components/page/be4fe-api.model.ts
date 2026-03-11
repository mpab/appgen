__ENTITY_REFERENCES_IMPORTS__
import { __ENTITY_PASCAL__View } from './__ENTITY_KEBAB__.view';
import { __ENTITY_PASCAL__Model as __ENTITY_PASCAL__Model } from './__ENTITY_KEBAB__.model';

export interface __ENTITY_PASCAL__ApiModel {
    version: {
        shape: string,
        major: number,
        minor: number,
        revision: number
    },
    entities: __ENTITY_PASCAL__Model[],
    views: __ENTITY_PASCAL__View[],
    entity_fields: string[],
    references: {
__ENTITY_REFERENCES_DECLARATIONS__
    }
};
