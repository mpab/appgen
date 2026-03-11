import { __ENTITY_PASCAL__ApiModel } from "./__ENTITY_KEBAB__-api.model";
import { __ENTITY_PASCAL__Model } from "./__ENTITY_KEBAB__.model";
import { __ENTITY_PASCAL__View } from "./__ENTITY_KEBAB__.view";

export class __ENTITY_PASCAL__ViewModel {
    static createView = (): __ENTITY_PASCAL__View => {
        return {
__CREATE_VIEW__
        };
    }

    static mapModelToView(apiModel: __ENTITY_PASCAL__ApiModel, model: __ENTITY_PASCAL__Model): __ENTITY_PASCAL__View {
        let view = Object.assign([] as unknown as __ENTITY_PASCAL__View, model);
        let x;
__MODEL_VIEW_MAPPERS__
        return view;
    }

    static mapViewToModel(apiModel: __ENTITY_PASCAL__ApiModel, view: __ENTITY_PASCAL__View): __ENTITY_PASCAL__Model {
        let model = Object.assign({} as __ENTITY_PASCAL__Model, view);
        let x;
__VIEW_MODEL_MAPPERS__
        return model;
    }
}