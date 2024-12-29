import { fetchUtils } from "react-admin";
import { stringify } from "query-string";
const apiUrl = "http://127.0.0.1:8004"; //FIXME, this should be an envar
const httpClient = fetchUtils.fetchJson;

interface GetListParams {
  sort: {
    field: string;
    order: string;
  };
}

interface GetOneParams {
  id: string | number;
}

const fastApiProvider = {
  getList: (resource: string, params: GetListParams) => {
    const { field, order } = params.sort;
    const query = {
      sort: field,
      order: order,
    };
    return httpClient(`${apiUrl}/${resource}?${stringify(query)}`).then(
      ({ json }) => ({
        data: json,
        total: json.length,
      }),
    );
  },

  getOne: (resource: string, params: GetOneParams) => {
    return httpClient(`${apiUrl}/${resource}/${params.id}`).then(
      ({ json }) => ({
        data: json,
      }),
    );
  },
};

export default fastApiProvider;
