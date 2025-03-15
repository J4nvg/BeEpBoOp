"use client"

import { useState } from "react"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import {
  Cpu,
  CircuitBoardIcon as Motherboard,
  CpuIcon as Gpu,
  MemoryStickIcon as Memory,
  HardDrive,
  Power,
  Fan,
  Square,
  type LucideIcon,
  Plus,
} from "lucide-react"
import { Button } from "@/components/ui/button"

interface Component {
  id: number | string
  name: string
  price: number
  specs: string
  imageUrl?: string
  type: string
}

interface ComponentType {
  id: string
  label: string
  icon: LucideIcon
}

// Static sample data for components
const sampleComponents: Component[] = [
  { id: 1, type: "cpu", name: "Intel Core i7-11700K", specs: "8 cores, 16 threads, 3.6 GHz", price: 320 },
  { id: 2, type: "cpu", name: "AMD Ryzen 5 5600X", specs: "6 cores, 12 threads, 3.7 GHz", price: 280 },
  { id: 10, type: "cpu", name: "AMD Ryzen 7 5800X", specs: "8 cores, 16 threads, 3.8 GHz", price: 350 },
  { id: 11, type: "cpu", name: "Intel Core i5-12600K", specs: "10 cores, 16 threads, 3.7 GHz", price: 290 },
  { id: 12, type: "cpu", name: "AMD Ryzen 9 5900X", specs: "12 cores, 24 threads, 3.7 GHz", price: 450 },
  { id: 13, type: "cpu", name: "Intel Core i9-12900K", specs: "16 cores, 24 threads, 3.2 GHz", price: 580 },
  { id: 14, type: "cpu", name: "AMD Ryzen 5 5600G", specs: "6 cores, 12 threads, 3.9 GHz", price: 260 },
  { id: 15, type: "cpu", name: "Intel Core i7-12700K", specs: "12 cores, 20 threads, 3.6 GHz", price: 410 },
  { id: 16, type: "cpu", name: "AMD Ryzen 7 5700G", specs: "8 cores, 16 threads, 3.8 GHz", price: 330 },
  { id: 3, type: "motherboard", name: "ASUS Prime B550-PLUS", specs: "ATX, AM4 socket", price: 150 },
  { id: 17, type: "motherboard", name: "MSI MAG B660 TOMAHAWK", specs: "ATX, LGA1700 socket", price: 180 },
  { id: 4, type: "gpu", name: "NVIDIA RTX 3080", specs: "10GB GDDR6X", price: 699 },
  { id: 5, type: "ram", name: "Corsair Vengeance LPX 16GB", specs: "DDR4 3200MHz", price: 80 },
  { id: 6, type: "storage", name: "Samsung 970 EVO Plus", specs: "1TB NVMe SSD", price: 130 },
  { id: 7, type: "power", name: "EVGA 600W Bronze", specs: "80+ Bronze Certification", price: 60 },
  { id: 8, type: "cooling", name: "Cooler Master Hyper 212", specs: "Air CPU Cooler", price: 35 },
  { id: 9, type: "case", name: "NZXT H510", specs: "Mid Tower, Tempered Glass", price: 70 },
]

// Component types definition
const componentTypes: ComponentType[] = [
  { id: "cpu", label: "CPU", icon: Cpu },
  { id: "motherboard", label: "Motherboard", icon: Motherboard },
  { id: "gpu", label: "GPU", icon: Gpu },
  { id: "ram", label: "RAM", icon: Memory },
  { id: "storage", label: "Storage", icon: HardDrive },
  { id: "power", label: "Power Supply", icon: Power },
  { id: "cooling", label: "Cooling", icon: Fan },
  { id: "case", label: "Case", icon: Square },
]

export default function PCBuilder() {
  const [selectedType, setSelectedType] = useState<string>("cpu")
  const [selectedComponents, setSelectedComponents] = useState<Record<string, Component | null>>({
    cpu: null,
    motherboard: null,
    gpu: null,
    ram: null,
    storage: null,
    power: null,
    cooling: null,
    case: null,
  })

  // Filter sample data based on the selected component type
  const availableComponents = sampleComponents.filter((component) => component.type === selectedType)

  // Add component to build
  const addToBuild = (component: Component) => {
    setSelectedComponents({
      ...selectedComponents,
      [component.type]: component,
    })
  }

  // Calculate total price
  const totalPrice = Object.values(selectedComponents)
    .filter(Boolean)
    .reduce((sum, component) => sum + (component?.price || 0), 0)

  return (
    <div className="container mx-auto p-6 max-w-5xl">
      <h1 className="text-3xl font-bold mb-8 text-center">PC Builder</h1>

      {/* Selected Components Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {componentTypes.map((type) => {
          const Icon = type.icon
          const selectedComponent = selectedComponents[type.id]

          return (
            <Card key={type.id} className="h-auto">
              <CardContent className="p-4">
                <div className="flex items-center gap-2">
                  <Icon className="w-5 h-5 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium">{type.label}</p>
                    {selectedComponent ? (
                      <p className="text-sm truncate">{selectedComponent.name}</p>
                    ) : (
                      <p className="text-xs text-muted-foreground italic">Not selected</p>
                    )}
                  </div>
                  {selectedComponent && (
                    <span className="text-xs font-semibold text-[#8CD50B]">${selectedComponent.price.toFixed(2)}</span>
                  )}
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Total Price */}
      <div className="flex justify-end mb-6">
        <Card className="w-full md:w-auto">
          <CardContent className="p-4">
            <div className="flex justify-between gap-8">
              <span className="font-medium">Total:</span>
              <span className="font-bold text-[#8CD50B]">${totalPrice.toFixed(2)}</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Component Type Tabs */}
      <Tabs value={selectedType} onValueChange={(value) => setSelectedType(value)} className="mb-6">
        <TabsList className="w-full h-full grid grid-cols-4 md:grid-cols-8 gap-2">
          {componentTypes.map((type) => {
            const Icon = type.icon
            return (
              <TabsTrigger
                key={type.id}
                value={type.id}
                className="flex flex-col items-center p-4 data-[state=active]:bg-[#8CD50B] data-[state=active]:text-white hover:cursor-pointer"
              >
                <Icon className="w-6 h-6 mb-1" />
                <span className="text-xs truncate">{type.label}</span>
              </TabsTrigger>
            )
          })}
        </TabsList>
      </Tabs>

      {/* Component List */}
      <div className="grid gap-4">
        {availableComponents.length === 0 ? (
          <div className="text-center p-4">No components available</div>
        ) : (
          availableComponents.map((component) => (
            <Card key={component.id} className="hover:border-[#8CD50B] transition-colors">
              <CardContent className="flex items-center p-4">
                <div className="w-20 h-20 bg-gray-200 rounded flex items-center justify-center mr-4">
                  <img
                    src={component.imageUrl || "/placeholder.svg?height=80&width=80"}
                    alt={component.name}
                    className="w-16 h-16 object-contain"
                  />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold">{component.name}</h3>
                  <p className="text-sm text-gray-600">{component.specs}</p>
                </div>
                <div className="text-lg font-bold text-[#8CD50B]">${component.price.toFixed(2)}</div>
              </CardContent>
              <CardFooter className="justify-end">
                <Button variant="outline" className="hover:cursor-pointer" onClick={() => addToBuild(component)}>
                  Add to build <Plus className="ml-2 h-4 w-4" />
                </Button>
              </CardFooter>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}

