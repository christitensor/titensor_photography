import SwiftUI
import CoreImage.CIFilterBuiltins

struct RegistrationRecord: Identifiable {
    let id = UUID()
    let controlNumber: Int
    let firstName: String
    let lastName: String
    let number: String
    let grade: String
    let sport: String
    let school: String
    let team: String
    let parentFirstName: String
    let parentLastName: String
    let parentPhone: String
    let parentEmail: String
    let paymentType: String
    let paymentAmount: String
    let notes: String
}

class RegistrationViewModel: ObservableObject {
    @Published var controlNumber: Int = 0
    @Published var records: [RegistrationRecord] = []

    private let context = CIContext()
    private let filter = CIFilter.qrCodeGenerator()

    func addRecord(firstName: String, lastName: String, number: String, grade: String, sport: String, school: String, team: String, parentFirstName: String, parentLastName: String, parentPhone: String, parentEmail: String, paymentType: String, paymentAmount: String, notes: String) {
        controlNumber += 1
        let record = RegistrationRecord(controlNumber: controlNumber,
                                        firstName: firstName,
                                        lastName: lastName,
                                        number: number,
                                        grade: grade,
                                        sport: sport,
                                        school: school,
                                        team: team,
                                        parentFirstName: parentFirstName,
                                        parentLastName: parentLastName,
                                        parentPhone: parentPhone,
                                        parentEmail: parentEmail,
                                        paymentType: paymentType,
                                        paymentAmount: paymentAmount,
                                        notes: notes)
        records.append(record)
        saveCSV(record: record)
        _ = generateQRCode(from: "\(controlNumber)_\(firstName)_\(lastName)_\(grade)_\(number)_\(sport)_\(school)_\(paymentAmount)_\(paymentType)")
    }

    private func generateQRCode(from string: String) -> UIImage? {
        let data = Data(string.utf8)
        filter.setValue(data, forKey: "inputMessage")
        if let outputImage = filter.outputImage,
           let cgimg = context.createCGImage(outputImage, from: outputImage.extent) {
            return UIImage(cgImage: cgimg)
        }
        return nil
    }

    private func csvPath() -> URL {
        let fm = FileManager.default
        let docs = fm.urls(for: .documentDirectory, in: .userDomainMask).first!
        return docs.appendingPathComponent("registration.csv")
    }

    private func saveCSV(record: RegistrationRecord) {
        let header = "control_number,first name,last name,number,grade,sport,school,team,parent_first_name,parent_last_name,parent_phone_number,parent_email,payment_type,payment_amount,notes\n"
        let row = "\(record.controlNumber),\(record.firstName),\(record.lastName),\(record.number),\(record.grade),\(record.sport),\(record.school),\(record.team),\(record.parentFirstName),\(record.parentLastName),\(record.parentPhone),\(record.parentEmail),\(record.paymentType),\(record.paymentAmount),\(record.notes)\n"
        let url = csvPath()
        if !FileManager.default.fileExists(atPath: url.path) {
            try? header.write(to: url, atomically: true, encoding: .utf8)
        }
        if let handle = try? FileHandle(forWritingTo: url) {
            handle.seekToEndOfFile()
            if let data = row.data(using: .utf8) {
                handle.write(data)
            }
            handle.closeFile()
        }
    }
}

struct ContentView: View {
    @StateObject private var viewModel = RegistrationViewModel()
    @State private var firstName = ""
    @State private var lastName = ""
    @State private var number = ""
    @State private var grade = ""
    @State private var sport = ""
    @State private var school = ""
    @State private var team = ""
    @State private var parentFirstName = ""
    @State private var parentLastName = ""
    @State private var parentPhone = ""
    @State private var parentEmail = ""
    @State private var paymentType = "Did not pay"
    @State private var paymentAmount = ""
    @State private var notes = ""

    private let paymentOptions = ["Cash", "Card", "Check", "Did not pay"]

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Athlete")) {
                    TextField("First Name", text: $firstName)
                    TextField("Last Name", text: $lastName)
                    TextField("Number", text: $number)
                    TextField("Grade", text: $grade)
                    TextField("Sport", text: $sport)
                    TextField("School", text: $school)
                    TextField("Team", text: $team)
                }
                Section(header: Text("Parent")) {
                    TextField("First Name", text: $parentFirstName)
                    TextField("Last Name", text: $parentLastName)
                    TextField("Phone", text: $parentPhone)
                    TextField("Email", text: $parentEmail)
                }
                Section(header: Text("Payment")) {
                    Picker("Type", selection: $paymentType) {
                        ForEach(paymentOptions, id: \.self) { option in
                            Text(option)
                        }
                    }
                    TextField("Amount", text: $paymentAmount)
                }
                Section(header: Text("Notes")) {
                    TextField("Notes", text: $notes)
                }
                Button("Submit") {
                    viewModel.addRecord(firstName: firstName,
                                        lastName: lastName,
                                        number: number,
                                        grade: grade,
                                        sport: sport,
                                        school: school,
                                        team: team,
                                        parentFirstName: parentFirstName,
                                        parentLastName: parentLastName,
                                        parentPhone: parentPhone,
                                        parentEmail: parentEmail,
                                        paymentType: paymentType,
                                        paymentAmount: paymentAmount,
                                        notes: notes)
                    firstName = ""
                    lastName = ""
                    number = ""
                    grade = ""
                    sport = ""
                    school = ""
                    team = ""
                    parentFirstName = ""
                    parentLastName = ""
                    parentPhone = ""
                    parentEmail = ""
                    paymentType = "Did not pay"
                    paymentAmount = ""
                    notes = ""
                }
            }
            .navigationTitle("Registration")
        }
    }
}

@main
struct RegistrationSwiftUIApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
