import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Heart, Database, Users, Activity, Plus, Edit, Trash2 } from 'lucide-react'
import './App.css'

function App() {
  const [activeDatabase, setActiveDatabase] = useState('sql')
  const [patients, setPatients] = useState([])
  const [treatments, setTreatments] = useState([])
  const [showAddPatient, setShowAddPatient] = useState(false)
  const [showAddTreatment, setShowAddTreatment] = useState(false)

  const [newPatient, setNewPatient] = useState({
    name: '',
    gender: '',
    dateOfBirth: '',
    status: 'Ativo',
    admissionDate: ''
  })

  const [newTreatment, setNewTreatment] = useState({
    patientId: '',
    treatmentName: '',
    medication: '',
    dosage: '',
    schedule: ''
  })

  const addPatient = () => {
    if (newPatient.name && newPatient.gender && newPatient.dateOfBirth && newPatient.admissionDate) {
      const patient = {
        id: Date.now(),
        ...newPatient
      }
      setPatients([...patients, patient])
      setNewPatient({
        name: '',
        gender: '',
        dateOfBirth: '',
        status: 'Ativo',
        admissionDate: ''
      })
      setShowAddPatient(false)
    }
  }

  const addTreatment = () => {
    if (newTreatment.patientId && newTreatment.treatmentName && newTreatment.medication) {
      const treatment = {
        id: Date.now(),
        ...newTreatment
      }
      setTreatments([...treatments, treatment])
      setNewTreatment({
        patientId: '',
        treatmentName: '',
        medication: '',
        dosage: '',
        schedule: ''
      })
      setShowAddTreatment(false)
    }
  }

  const deletePatient = (id) => {
    setPatients(patients.filter(p => p.id !== id))
  }

  const deleteTreatment = (id) => {
    setTreatments(treatments.filter(t => t.id !== id))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Heart className="h-8 w-8 text-red-500" />
            <h1 className="text-4xl font-bold text-gray-800">Monitor de Tratamento de Pacientes Hospitalares</h1>
          </div>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Sistema abrangente de monitoramento de tratamento de pacientes para profissionais de saúde 
            com operações CRUD completas em dados de pacientes e registros médicos
          </p>
        </div>

        {/* Database Management Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Database className="h-5 w-5" />
              Gerenciamento de Banco de Dados
            </CardTitle>
            <CardDescription>
              Escolha entre gerenciamento de banco de dados SQL (dados de Paciente/Tratamento) e NoSQL (Registros Médicos/Consultas)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Button
                variant={activeDatabase === 'sql' ? 'default' : 'outline'}
                className="h-16 text-left justify-start"
                onClick={() => setActiveDatabase('sql')}
              >
                <div>
                  <div className="font-semibold">Banco de Dados SQL</div>
                  <div className="text-sm opacity-70">SQLite</div>
                </div>
              </Button>
              <Button
                variant={activeDatabase === 'nosql' ? 'default' : 'outline'}
                className="h-16 text-left justify-start"
                onClick={() => setActiveDatabase('nosql')}
              >
                <div>
                  <div className="font-semibold">Banco de Dados NoSQL</div>
                  <div className="text-sm opacity-70">JSON</div>
                </div>
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Database Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Card className="bg-blue-50 border-blue-200">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-blue-700">
                <Users className="h-5 w-5" />
                Banco de Dados de Pacientes
              </CardTitle>
              <CardDescription>
                Gerencie registros de pacientes com informações pessoais, histórico médico e detalhes de admissão
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="bg-green-50 border-green-200">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-green-700">
                <Activity className="h-5 w-5" />
                Banco de Dados de Tratamentos
              </CardTitle>
              <CardDescription>
                Acompanhe tratamentos ativos, medicamentos, dosagens e cronogramas de tratamento
              </CardDescription>
            </CardHeader>
          </Card>
        </div>

        {/* SQL Database Management */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-red-600">
              <Heart className="h-5 w-5" />
              Gerenciamento de Banco de Dados SQL
            </CardTitle>
            <CardDescription>
              Gerencie pacientes e tratamentos no banco de dados SQLite
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <Button
                variant="outline"
                className="h-16 justify-between"
                onClick={() => setShowAddPatient(!showAddPatient)}
              >
                <div className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  <span>Pacientes ({patients.length})</span>
                </div>
                <Badge variant="secondary">{patients.length}</Badge>
              </Button>
              <Button
                variant="outline"
                className="h-16 justify-between"
                onClick={() => setShowAddTreatment(!showAddTreatment)}
              >
                <div className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  <span>Tratamentos ({treatments.length})</span>
                </div>
                <Badge variant="secondary">{treatments.length}</Badge>
              </Button>
            </div>

            {/* Patient Records Section */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold">Registros de Pacientes</h3>
                <Button onClick={() => setShowAddPatient(!showAddPatient)} className="flex items-center gap-2">
                  <Plus className="h-4 w-4" />
                  Adicionar Paciente
                </Button>
              </div>
              <p className="text-gray-600 mb-4">Gerencie informações de pacientes e detalhes de admissão</p>

              {/* Add Patient Form */}
              {showAddPatient && (
                <Card className="mb-4 bg-blue-50">
                  <CardHeader>
                    <CardTitle>Adicionar Novo Paciente</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <input
                        type="text"
                        placeholder="Nome completo"
                        value={newPatient.name}
                        onChange={(e) => setNewPatient({...newPatient, name: e.target.value})}
                        className="p-2 border rounded"
                      />
                      <select
                        value={newPatient.gender}
                        onChange={(e) => setNewPatient({...newPatient, gender: e.target.value})}
                        className="p-2 border rounded"
                      >
                        <option value="">Selecionar Gênero</option>
                        <option value="Masculino">Masculino</option>
                        <option value="Feminino">Feminino</option>
                        <option value="Outro">Outro</option>
                      </select>
                      <input
                        type="date"
                        placeholder="Data de Nascimento"
                        value={newPatient.dateOfBirth}
                        onChange={(e) => setNewPatient({...newPatient, dateOfBirth: e.target.value})}
                        className="p-2 border rounded"
                      />
                      <select
                        value={newPatient.status}
                        onChange={(e) => setNewPatient({...newPatient, status: e.target.value})}
                        className="p-2 border rounded"
                      >
                        <option value="Ativo">Ativo</option>
                        <option value="Inativo">Inativo</option>
                        <option value="Alta">Alta</option>
                      </select>
                      <input
                        type="date"
                        placeholder="Data de Admissão"
                        value={newPatient.admissionDate}
                        onChange={(e) => setNewPatient({...newPatient, admissionDate: e.target.value})}
                        className="p-2 border rounded"
                      />
                    </div>
                    <div className="flex gap-2 mt-4">
                      <Button onClick={addPatient}>Salvar Paciente</Button>
                      <Button variant="outline" onClick={() => setShowAddPatient(false)}>Cancelar</Button>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Patients Table */}
              <div className="overflow-x-auto">
                <table className="w-full border-collapse border border-gray-300">
                  <thead>
                    <tr className="bg-gray-100">
                      <th className="border border-gray-300 p-2 text-left">ID do Paciente</th>
                      <th className="border border-gray-300 p-2 text-left">Nome</th>
                      <th className="border border-gray-300 p-2 text-left">Gênero</th>
                      <th className="border border-gray-300 p-2 text-left">Data de Nascimento</th>
                      <th className="border border-gray-300 p-2 text-left">Status</th>
                      <th className="border border-gray-300 p-2 text-left">Data de Admissão</th>
                      <th className="border border-gray-300 p-2 text-left">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {patients.length === 0 ? (
                      <tr>
                        <td colSpan="7" className="border border-gray-300 p-4 text-center text-gray-500">
                          Nenhum paciente cadastrado
                        </td>
                      </tr>
                    ) : (
                      patients.map((patient) => (
                        <tr key={patient.id}>
                          <td className="border border-gray-300 p-2">{patient.id}</td>
                          <td className="border border-gray-300 p-2">{patient.name}</td>
                          <td className="border border-gray-300 p-2">{patient.gender}</td>
                          <td className="border border-gray-300 p-2">{patient.dateOfBirth}</td>
                          <td className="border border-gray-300 p-2">
                            <Badge variant={patient.status === 'Ativo' ? 'default' : 'secondary'}>
                              {patient.status}
                            </Badge>
                          </td>
                          <td className="border border-gray-300 p-2">{patient.admissionDate}</td>
                          <td className="border border-gray-300 p-2">
                            <div className="flex gap-2">
                              <Button size="sm" variant="outline">
                                <Edit className="h-4 w-4" />
                              </Button>
                              <Button size="sm" variant="destructive" onClick={() => deletePatient(patient.id)}>
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Treatments Section */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold">Registros de Tratamentos</h3>
                <Button onClick={() => setShowAddTreatment(!showAddTreatment)} className="flex items-center gap-2">
                  <Plus className="h-4 w-4" />
                  Adicionar Tratamento
                </Button>
              </div>
              <p className="text-gray-600 mb-4">Gerencie tratamentos ativos e medicações</p>

              {/* Add Treatment Form */}
              {showAddTreatment && (
                <Card className="mb-4 bg-green-50">
                  <CardHeader>
                    <CardTitle>Adicionar Novo Tratamento</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <select
                        value={newTreatment.patientId}
                        onChange={(e) => setNewTreatment({...newTreatment, patientId: e.target.value})}
                        className="p-2 border rounded"
                      >
                        <option value="">Selecionar Paciente</option>
                        {patients.map((patient) => (
                          <option key={patient.id} value={patient.id}>
                            {patient.name} (ID: {patient.id})
                          </option>
                        ))}
                      </select>
                      <input
                        type="text"
                        placeholder="Nome do Tratamento"
                        value={newTreatment.treatmentName}
                        onChange={(e) => setNewTreatment({...newTreatment, treatmentName: e.target.value})}
                        className="p-2 border rounded"
                      />
                      <input
                        type="text"
                        placeholder="Medicamento"
                        value={newTreatment.medication}
                        onChange={(e) => setNewTreatment({...newTreatment, medication: e.target.value})}
                        className="p-2 border rounded"
                      />
                      <input
                        type="text"
                        placeholder="Dosagem"
                        value={newTreatment.dosage}
                        onChange={(e) => setNewTreatment({...newTreatment, dosage: e.target.value})}
                        className="p-2 border rounded"
                      />
                      <input
                        type="text"
                        placeholder="Cronograma (ex: 3x ao dia)"
                        value={newTreatment.schedule}
                        onChange={(e) => setNewTreatment({...newTreatment, schedule: e.target.value})}
                        className="p-2 border rounded col-span-1 md:col-span-2"
                      />
                    </div>
                    <div className="flex gap-2 mt-4">
                      <Button onClick={addTreatment}>Salvar Tratamento</Button>
                      <Button variant="outline" onClick={() => setShowAddTreatment(false)}>Cancelar</Button>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Treatments Table */}
              <div className="overflow-x-auto">
                <table className="w-full border-collapse border border-gray-300">
                  <thead>
                    <tr className="bg-gray-100">
                      <th className="border border-gray-300 p-2 text-left">ID do Tratamento</th>
                      <th className="border border-gray-300 p-2 text-left">ID do Paciente</th>
                      <th className="border border-gray-300 p-2 text-left">Nome do Tratamento</th>
                      <th className="border border-gray-300 p-2 text-left">Medicamento</th>
                      <th className="border border-gray-300 p-2 text-left">Dosagem</th>
                      <th className="border border-gray-300 p-2 text-left">Cronograma</th>
                      <th className="border border-gray-300 p-2 text-left">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {treatments.length === 0 ? (
                      <tr>
                        <td colSpan="7" className="border border-gray-300 p-4 text-center text-gray-500">
                          Nenhum tratamento cadastrado
                        </td>
                      </tr>
                    ) : (
                      treatments.map((treatment) => (
                        <tr key={treatment.id}>
                          <td className="border border-gray-300 p-2">{treatment.id}</td>
                          <td className="border border-gray-300 p-2">{treatment.patientId}</td>
                          <td className="border border-gray-300 p-2">{treatment.treatmentName}</td>
                          <td className="border border-gray-300 p-2">{treatment.medication}</td>
                          <td className="border border-gray-300 p-2">{treatment.dosage}</td>
                          <td className="border border-gray-300 p-2">{treatment.schedule}</td>
                          <td className="border border-gray-300 p-2">
                            <div className="flex gap-2">
                              <Button size="sm" variant="outline">
                                <Edit className="h-4 w-4" />
                              </Button>
                              <Button size="sm" variant="destructive" onClick={() => deleteTreatment(treatment.id)}>
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center text-gray-500 text-sm">
          <p>Feito com Manus</p>
        </div>
      </div>
    </div>
  )
}

export default App

