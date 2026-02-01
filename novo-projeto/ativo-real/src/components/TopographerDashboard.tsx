// @ts-nocheck
import React, { useState, useEffect } from 'react';
// @ts-ignore - antd types will be fixed
import { Button, Table, Modal, Form, Input, Select, message } from 'antd';
import { GlobalMap } from './GlobalMap';

/**
 * TopographerDashboard.tsx
 * Main dashboard for topographers (project management)
 */

export const TopographerDashboard: React.FC = () => {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedProject, setSelectedProject] = useState<any>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await fetch('/api/projects', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
      });
      const data = await response.json();
      setProjects(data);
    } catch (err) {
      message.error('Erro ao carregar projetos');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = async (values: any) => {
    try {
      const response = await fetch('/api/projects', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify(values),
      });
      const data = await response.json();
      message.success('Projeto criado!');
      setProjects([...projects, data]);
      setModalVisible(false);
      form.resetFields();
    } catch (err) {
      message.error('Erro ao criar projeto');
    }
  };

  const columns = [
    { title: 'Nome', dataIndex: 'nome', key: 'nome' },
    { title: 'Tipo', dataIndex: 'tipo', key: 'tipo' },
    { title: 'Status', dataIndex: 'status', key: 'status' },
    { title: 'Área (ha)', dataIndex: 'area_ha', key: 'area_ha' },
    {
      title: 'Ações',
      key: 'actions',
      render: (_, record) => (
        <Button
          type="link"
          onClick={() => setSelectedProject(record)}
        >
          Detalhes
        </Button>
      ),
    },
  ];

  if (loading) return <div className="p-4">Carregando...</div>;

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">📊 Dashboard do Topógrafo</h1>

      <div className="flex justify-between items-center">
        <p className="text-gray-600">Total de projetos: {projects.length}</p>
        <Button type="primary" onClick={() => setModalVisible(true)}>
          ➕ Novo Projeto
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={projects}
        loading={loading}
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />

      {/* Project Details Modal */}
      {selectedProject && (
        <Modal
          title={`Projeto: ${selectedProject.nome}`}
          visible={!!selectedProject}
          onCancel={() => setSelectedProject(null)}
          width={900}
          footer={null}
        >
          <div className="space-y-4">
            <GlobalMap projectId={selectedProject.id} />
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="font-semibold">Tipo</p>
                <p>{selectedProject.tipo}</p>
              </div>
              <div>
                <p className="font-semibold">Status</p>
                <p>{selectedProject.status}</p>
              </div>
              <div>
                <p className="font-semibold">Área</p>
                <p>{selectedProject.area_ha} ha</p>
              </div>
              <div>
                <p className="font-semibold">Municip ício</p>
                <p>{selectedProject.municipio}</p>
              </div>
            </div>
          </div>
        </Modal>
      )}

      {/* Create Project Modal */}
      <Modal
        title="Novo Projeto"
        visible={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreateProject}
        >
          <Form.Item
            label="Nome"
            name="nome"
            rules={[{ required: true, message: 'Campo obrigatório' }]}
          >
            <Input placeholder="Nome do projeto" />
          </Form.Item>

          <Form.Item
            label="Tipo"
            name="tipo"
            rules={[{ required: true }]}
          >
            <Select
              options={[
                { label: 'Individual', value: 'INDIVIDUAL' },
                { label: 'Desmembramento', value: 'DESMEMBRAMENTO' },
                { label: 'Loteamento', value: 'LOTEAMENTO' },
              ]}
            />
          </Form.Item>

          <Form.Item
            label="Área (ha)"
            name="area_ha"
            rules={[{ required: true }]}
          >
            <Input type="number" placeholder="0.00" />
          </Form.Item>

          <Form.Item
            label="Município"
            name="municipio"
            rules={[{ required: true }]}
          >
            <Input placeholder="São Paulo" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};
