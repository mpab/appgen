        this.__KEY_CAMEL__Service.read()
            .subscribe(response =>
                this.handleResponse(response, () => this.__KEY_CAMEL__Collection = response.result)
            );