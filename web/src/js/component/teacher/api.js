const baseUrl = '/api/teacher';

export const query_entities = async (page, size, keyword) => {
    let url = baseUrl;
    return window.Vue.http.get(url, {
        params: {
            page: page,
            size: size,
            keyword: keyword,
        }
    }).then(response => {
        if (response.ok) {
            return response.data;
        }
        else {

        }
    });
};

export const query_entity = async id => {
    let url = `${baseUrl}/${id}`;
    return window.Vue.http.get(url).then(response => {
        if (response.ok) {
            return response.data;
        }
    });
};

export const create_entity = async entity => {
    let url = baseUrl;
    // 新建
    return window.Vue.http.post(url, entity).then(response => {
        if (response.ok) {
            return response.data.result;
        }
    });
};

export const modify_entity = async entity => {
    let url = `${baseUrl}/${entity['Id']}`;
    // 修改
    return window.Vue.http.put(url, entity).then(response => {
        if (response.ok) {
            return response.data.result;
        }
    });
};

export const remove_entity = async entity => {
    let url = `${baseUrl}/${entity['Id']}`;
    return window.Vue.http.delete(url).then(response => {
        if (response.ok) {
            return response.data.result;
        }
    });
};