import { List, Datagrid, TextField, DateField } from 'react-admin';

export const TaskList = () => (
    <List pagination={false} title="Task Dashboard">
        <Datagrid>
            <TextField source="id" />
            <TextField source="state" />
            <TextField source="result" />
            <TextField source="date" showTime={true} />
        </Datagrid>
    </List>
);
